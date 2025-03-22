from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
from huggingface_hub import InferenceClient
import google.generativeai as genai
import json
import os, re, time
from .pinecone_integr import embedding_model, index
import uuid
from users.models import Resume
repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
client = InferenceClient(model=repo_id, token=os.getenv('HUGGINGFACE_API_KEY'))
def extract_text(file_path):
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    else:
        raise ValueError("Unsupport file format")
 
# load_dotenv()  
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def Parse_resume(text):
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Gemini API key is not set.")
    prompt = f"""
        Extract the following information from the CV below and return a valid JSON object:
    
    {{
        "name": "Full name of the candidate",
        "contact": {{
            "phone": "Phone number",
            "email": "Email address",
        }},
        "education": [
            {{
                "degree": "Degree title",
                "institution": "University or school name",
                "year": "Year of completion"
            }}
        ],
        "work_experience": [
            {{
                "company": "Company name",
                "role": "Job title",
                "duration": "Start and end dates",
                "projects": "Key projects and contributions"
            }}
        ],
        "skills": ["Skill1", "Skill2", "Skill3"]
    }}

    Only return JSON. Do not include explanations or text outside this JSON.

    CV Text:
    {text}
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    cleaned_text = re.sub(r"```json|```", "", response.text).strip()

    try:
        parsed_info = json.loads(cleaned_text)
    except json.JSONDecodeError:
        print("API returned invalid JSON. Check response format.")
        parsed_info = {"error": "Invalid API response", "raw_response": cleaned_text}
    

    return parsed_info


def parse_job_description(jd_text, retries=3):
    """
    Parse a job description into structured JSON format using the Gemini API.
    Implements retry logic with exponential backoff to handle rate limits.

    Parameters:
        jd_text (str): The job description text to parse.
        retries (int): Number of retry attempts for API failures.

    Returns:
        dict: Parsed job description as a dictionary or an error dictionary.
    """
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Gemini API key is not set.")

    prompt = f"""
    Extract the following structured information from the job description below and return a valid JSON object:
    
    {{
        "job_title": "Job title mentioned in the description",
        "employment_type": "Full-time, Part-time, Contract, Internship, etc.",
        "education_requirements": "Required education"
        "description": "Overall job description",
        "experience_level": "Entry-level, Mid-level, Senior, etc.",
        "required_skills": ["Skill1", "Skill2", "Skill3"]
    }}

    Only return JSON. Do not include explanations or text outside this JSON.

    Job Description Text:
    {jd_text}
    """

    model = genai.GenerativeModel("gemini-1.5-pro")

    for attempt in range(retries):
        try:
            # Generate response from Gemini API
            response = model.generate_content(prompt)
            cleaned_text = re.sub(r"```json|```", "", response.text).strip()

            # Parse the cleaned text into JSON
            parsed_job = json.loads(cleaned_text)
            return parsed_job

        except json.JSONDecodeError:
            print(f"Attempt {attempt + 1}: API returned invalid JSON. Retrying...")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Failed to parse job description after retries.")
                return {"error": "Invalid API response", "raw_response": cleaned_text}

        except Exception as e:
            print(f"Attempt {attempt + 1}: Error parsing job description - {e}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Failed to parse job description after retries.")
                return {"error": str(e), "raw_response": response.text if 'response' in locals() else None}

    return {"error": "All retry attempts failed", "raw_response": None}

def get_jd_embedding(jd_data, retries=3):
    """
    Convert structured job description data into a meaningful text representation
    and generate embeddings.
    """
    text_representation = f"""
    Job Title: {jd_data.get('job_title', 'Unknown')}
    Required Skills: {', '.join(jd_data.get('required_skills', []))}
    Responsibilities: {', '.join(jd_data.get('responsibilities', []))}
    Qualifications: {', '.join(jd_data.get('qualifications', []))}
    """
    for attempt in range(retries):
        try:
            return embedding_model.encode(text_representation, convert_to_tensor=True)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Failed to generate embedding after retries.")
                return None
            
def store_jd_embedding(jd_id,jd_embedding):
    """
    Store job description embeddings in Pinecone with error handling.
    If no ID is provided, generate a UUID.
    """
    if jd_id is None:
        jd_id = str(uuid.uuid4())  # Generate a unique ID if not provided
    try:
        index.upsert([(jd_id, jd_embedding.tolist())])
        print(f"Successfully stored JD embedding f")
    except Exception as e:
        print(f"Failed to store JD embedding : {e}")


def get_cv_embedding(cv_data, retries=3, timeout=10):
    """
    Convert structured CV data into text representation and generate embeddings with retry logic.
    
    Parameters:
        cv_data (dict): Parsed CV data.
        retries (int): Number of retry attempts for API failures.
    
    Returns:
        tensor: Embedding tensor or None if failed.
    """
    text_representation = f"""
    Name: {cv_data.get('name', 'Unknown')}
    Education: {', '.join([f"{edu.get('degree', '')} from {edu.get('institution', '')}" for edu in cv_data.get('education', []) if edu.get('degree') and edu.get('institution')])}
    Work Experience: {', '.join([f"{job.get('role', '')} at {job.get('company', '')}" for job in cv_data.get('work_experience', []) if job.get('role') and job.get('company')])}
    Skills: {', '.join([skill for skill in cv_data.get('skills', []) if skill])}
    """

    # print("text representa : ",text_representation,flush=True)
    start_time = time.time()
    for attempt in range(retries):
        try:
            return embedding_model.encode(text_representation, convert_to_tensor=True)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1 and (time.time() - start_time) < timeout:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Failed to generate embedding after retries.")
                return None

def clear_pinecone():
    """
    Clear all data in Pinecone index.
    """
    try:
        # Clear the entire index by deleting all IDs
        index.delete(delete_all=True)  # Deleting all items in the index
        print("Successfully cleared Pinecone index.")
    except Exception as e:
        print(f"Failed to clear Pinecone index: {e}")

def store_cv_embedding(cv_id, cv_embedding):
    """
    Store candidate embeddings in Pinecone with error handling.
    """
    try:
        index.upsert([(cv_id, cv_embedding.tolist())])
        print(f"Successfully stored CV embedding for ID: {cv_id}")
    except Exception as e:
        print(f"Failed to store CV embedding for ID {cv_id}: {e}")


def summarize_text(text):
    """
    Generate a summary of the input text using the Mixtral model.
    """

    prompt = f"""
    Summarize the following text into a concise and complete paragraph. Focus only on:
    - Current role or academic status
    - Educational background
    - Relevant work experience
    - Technical skills and expertise

    Exclude any information about spoken languages, hobbies, or interests. Ensure the summary is well-structured and does not exceed 50 words:
    
    {text}
    """
    response = client.text_generation(prompt)
    return response

def rank_candidates(jd_embedding, exclude_id=None,n=10):
    """
    Retrieve and rank all candidates, even those with no match (score 0), from Pinecone.
    Exclude a specific ID (e.g., the job description itself).

    Parameters:
        jd_embedding (np.array): Embedding of the job description.
        exclude_id (str): ID to exclude from ranking (e.g., job description ID).

    Returns:
        list: Ranked candidates with similarity scores (including 0 for non-matches).
    """
    try:
        # Query Pinecone for similar embeddings
        results = index.query(
            vector=jd_embedding.tolist(),
            top_k=n,
            include_values=True,
            include_metadata=True 
        )

        ranked_candidates = []
        for match in results['matches']:
            if match['id'] != exclude_id:
                similarity_score = match.get('score', 0)  
                similarity_percentage = round(similarity_score * 100, 2)  
                resume = Resume.objects.get(id=match['id'])  # Query for resume by ID
                resume.score = similarity_percentage  # Update the score
                resume.save()
                ranked_candidates.append({
                    "candidate_id": match['id'],
                    "similarity_score": similarity_percentage  
                })
        # Sort candidates by similarity score in descending order
        ranked_candidates = sorted(
            ranked_candidates,
            key=lambda x: x["similarity_score"],
            reverse=True
        )

        return ranked_candidates

    except Exception as e:
        print(f"Error ranking candidates: {e}")
        return None

def compare_skills(job_skills, candidate_skills):
    """
    Compare skills between a job description and a candidate profile.

    Parameters:
        job_skills (list): List of skills required by the job description.
        candidate_skills (list): List of skills in the candidate's profile.

    Returns:
        dict: A dictionary containing matched, missing, and extra skills.
    """
    # Convert lists to sets for comparison
    job_skills_set = set(job_skills)
    candidate_skills_set = set(candidate_skills)

    matched_skills = list(job_skills_set.intersection(candidate_skills_set))
    missing_skills = list(job_skills_set - candidate_skills_set)
    extra_skills = list(candidate_skills_set - job_skills_set)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills
    }

def extract_skill_embeddings(skill_names, text_embeddings, skill_to_index):
    """
    Extract embeddings for specific skills from the full text embeddings.

    Parameters:
        skill_names (list): List of skill names.
        text_embeddings (np.array): Embeddings for the full text.
        skill_to_index (dict): Mapping of skill names to their positions in the text.

    Returns:
        np.array: Embeddings for the specified skills.
    """
    skill_indices = [skill_to_index[skill] for skill in skill_names]
    return text_embeddings[skill_indices]

def compare_skill_embeddings(job_skills, candidate_skills, threshold=0.8):
    """
    Compare job skills and candidate skills using embeddings.

    Parameters:
        job_skills (list): List of job skill names.
        candidate_skills (list): List of candidate skill names.
        threshold (float): Similarity threshold for matching skills.

    Returns:
        dict: A dictionary containing matched, missing, and extra skills.
    """
    job_skill_embeddings = embedding_model.encode(job_skills, convert_to_tensor=True)

    candidate_skill_embeddings = embedding_model.encode(candidate_skills, convert_to_tensor=True)

    similarity_matrix = cosine_similarity(job_skill_embeddings.cpu().numpy(), candidate_skill_embeddings.cpu().numpy())

    # Find matched, missing, and extra skills
    matched_skills = []
    missing_skills = []
    extra_skills = candidate_skills.copy()

    for i, job_skill in enumerate(job_skills):
        max_similarity = np.max(similarity_matrix[i])
        if max_similarity >= threshold:
            matched_index = np.argmax(similarity_matrix[i])
            matched_skill = candidate_skills[matched_index]
            matched_skills.append((job_skill, matched_skill))
            extra_skills.remove(matched_skill)
        else:
            missing_skills.append(job_skill)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills
    }