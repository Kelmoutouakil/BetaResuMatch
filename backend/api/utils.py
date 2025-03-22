from PyPDF2 import PdfReader
from huggingface_hub import InferenceClient
from PIL import Image
import pytesseract
import google.generativeai as genai
import json
import os, re, time
from .pinecone_integr import embedding_model, index
import uuid
repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
client = InferenceClient(model=repo_id, token=os.getenv('HUGGINGFACE_API_KEY'))
def extract_text(file_path):
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    # elif file_path.endswitch(('.png', '.jpg', '.jpeg')):
    #     image = Image.open(file_path)
    #     text = pytesseract.image_to_string(image)
    #     print("----text : ",text, flush=True)
    #     return text
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

def rank_candidates(jd_embedding, exclude_id=None):
    """
    Retrieve the top matching candidates from Pinecone and rank them.
    Exclude a specific ID (e.g., the job description itself).

    Parameters:
        jd_embedding (np.array): Embedding of the job description.
        exclude_id (str): ID to exclude from ranking (e.g., job description ID).

    Returns:
        list: Ranked candidates with similarity scores.
    """
    try:
        # Query Pinecone for similar embeddings
        results = index.query(
            vector=jd_embedding.tolist(),
            top_k=10,
            include_values=True
        )

        # Filter out the excluded ID (e.g., job description)
        ranked_candidates = []
        for match in results['matches']:
            if match['id'] != exclude_id:  # Exclude the job description
                similarity_percentage = round(match['score'] * 100, 2)  # Convert score to percentage
                ranked_candidates.append({
                    "candidate_id": match['id'],
                    "similarity_score": similarity_percentage  # Keep as numerical value for sorting
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