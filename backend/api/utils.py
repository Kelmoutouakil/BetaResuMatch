from PyPDF2 import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
from huggingface_hub import InferenceClient
import google.generativeai as genai
import json
import numpy as np
import os, re, time
from .pinecone_integr import embedding_model, index
import uuid
from users.models import Resume

repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
client = InferenceClient(model=repo_id, token=os.getenv('HUGGINGFACE_API_KEY'))
def extract_text(uploaded_file):
    print("------------extract-----",flush=True)
#     if file_path.endswith('.pdf'):
#         reader = PdfReader(file_path)
#         text = ''
#         for page in reader.pages:
#             text += page.extract_text()
#         return text
#     else:
#         raise ValueError("Unsupport file format")
    if not uploaded_file.name.endswith('.pdf'):
        raise ValueError("Unsupported file format")

    reader = PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"
    print("-------text---",text,flush=True)
    return text

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def Parse_resume(text):
    print("*****************",flush=True)
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
        "skills": ["Skill1", "Skill2", "Skill3"],
        "job_title": "Current or most recent job title",
        "latest_school": "Current or most recent school",
        "desired_role": "Desired role or internship title"
    }}

    Only return JSON. Do not include explanations or text outside this JSON.

    CV Text:
    {text}
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    cleaned_text = re.sub(r"```json|```", "", response.text).strip()

    try:
        parsed_info = json.loads(cleaned_text)
        print("parsed info",parsed_info,flush=True)
    except json.JSONDecodeError:
        print("---error: from pars resume ---",flush=True)
        print("API returned invalid JSON. Check response format.",flush=True)
        parsed_info = {"error": "Invalid API response", "raw_response": cleaned_text}
    
    return parsed_info



def parse_job_description(jd_text, retries=3):
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

    model = genai.GenerativeModel("gemini-1.5-flash")

    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            cleaned_text = re.sub(r"```json|```", "", response.text).strip()
            parsed_job = json.loads(cleaned_text)
            return parsed_job

        except json.JSONDecodeError:
            print(f"Attempt {attempt + 1}: API returned invalid JSON. Retrying...")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  
                print(f"Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Failed to parse job description after retries.")
                return {"error": "Invalid API response", "raw_response": cleaned_text}

        except Exception as e:
            print(f"Attempt {attempt + 1}: Error parsing job description - {e}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  
                print(f"Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Failed to parse job description after retries.")
                return {"error": str(e), "raw_response": response.text if 'response' in locals() else None}

    return {"error": "All retry attempts failed", "raw_response": None}

def get_jd_embedding(jd_data, retries=3):
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
                wait_time = 2 ** attempt 
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Failed to generate embedding after retries.")
                return None
            
def store_jd_embedding(jd_id,jd_embedding):

    if jd_id is None:
        jd_id = str(uuid.uuid4())  
    try:
        index.upsert([(jd_id, jd_embedding.tolist())])
        print(f"Successfully stored JD embedding f")
    except Exception as e:
        print(f"Failed to store JD embedding : {e}")



def get_cv_embedding(cv_data, retries=3, timeout=10):

    if isinstance(cv_data, dict):

        name = cv_data.get("name", "Unknown")
        education = cv_data.get("education", [])
        work_experience = cv_data.get("work_experience", [])
        skills = cv_data.get("skills", [])
        job_title = cv_data.get("job_title", "Unknown")
        latest_school = cv_data.get("latest_school", "Unknown")
        desired_role = cv_data.get("desired_role", "Unknown")
        education_text = ", ".join([
            f"{edu.get('degree', 'Unknown Degree')} from {edu.get('institution', 'Unknown Institution')}"
            for edu in education
        ])

        work_experience_text = ", ".join([
            f"{job.get('role', 'Unknown Role')} at {job.get('company', 'Unknown Company')}"
            for job in work_experience
        ])

        skills_text = ", ".join(skills)

        text_representation = f"""
        Name: {name}
        Job Title: {job_title}
        Latest School: {latest_school}
        Desired Role: {desired_role}
        Education: {education_text}
        Work Experience: {work_experience_text}
        Skills: {skills_text}
        """
    elif isinstance(cv_data, list):
        text_representation = f"Skills: {', '.join(cv_data)}"
    else:
        raise ValueError("Input must be a dictionary or a list of skills.")
    start_time = time.time()
    for attempt in range(retries):
        try:
            embedding = embedding_model.encode(text_representation, convert_to_tensor=True)
            return embedding
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1 and (time.time() - start_time) < timeout:
                wait_time = 2 ** attempt 
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Failed to generate embedding after retries.")
                return None
            
def clear_pinecone():
    try:
        index.delete(delete_all=True)  
        print("Successfully cleared Pinecone index.")
    except Exception as e:
        print(f"Failed to clear Pinecone index: {e}")

def store_cv_embedding(cv_id, cv_embedding):
    try:
        index.upsert([(cv_id, cv_embedding.tolist())])
        print(f"Successfully stored CV embedding for ID: {cv_id}")
    except Exception as e:
        print(f"Failed to store CV embedding for ID {cv_id}: {e}")


def summarize_text(text):
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

def rank_candidates(jd_embedding, exclude_id=None,n=20):
    try:
        results = index.query(
            vector=jd_embedding.tolist(),
            top_k=n,
            include_values=True
        )
        for match in results['matches']:
            if match['id'] != '-1' and  match['id'] != exclude_id  :
                resume =  Resume.objects.get(id=match['id'])

                similarity_percentage = round(match['score'] * 100, 2)  
                resume.score = similarity_percentage
                resume.save()
    except Exception as e:
        print(f"Error ranking candidates: {e}")




def extract_skill_embeddings(skill_names, text_embeddings, skill_to_index):

    skill_indices = [skill_to_index[skill] for skill in skill_names]
    return text_embeddings[skill_indices]

# def compare_skill_embeddings(job_skills, candidate_skills, threshold=0.8):
 
#     if job_skills and candidate_skills:
#         job_skill_embeddings = embedding_model.encode(job_skills, convert_to_tensor=True)

#         candidate_skill_embeddings = embedding_model.encode(candidate_skills, convert_to_tensor=True)

#         similarity_matrix = cosine_similarity(job_skill_embeddings.cpu().numpy(), candidate_skill_embeddings.cpu().numpy())

#         matched_skills = []
#         missing_skills = []
#         extra_skills = candidate_skills.copy()

#         for i, job_skill in enumerate(job_skills):
#             max_similarity = np.max(similarity_matrix[i])
#             if max_similarity >= threshold:
#                 matched_index = np.argmax(similarity_matrix[i])
#                 matched_skill = candidate_skills[matched_index]
#                 matched_skills.append((job_skill, matched_skill))
#                 extra_skills.remove(matched_skill)
#             else:
#                 missing_skills.append(job_skill)

#     return {
#         "matched_skills": matched_skills,
#         "missing_skills": missing_skills,
#         "extra_skills": extra_skills
#     }
def compare_skill_embeddings(job_skills, candidate_skills, threshold=0.8):
    """
    Compare job skills and candidate skills using embeddings with robust error handling.

    Parameters:
        job_skills (list): List of job skill names.
        candidate_skills (list): List of candidate skill names.
        threshold (float): Similarity threshold for matching skills.

    Returns:
        dict: A dictionary containing matched, missing, and extra skills.
    """
    # Handle empty inputs
    if not job_skills or not candidate_skills:
        return {
            "matched_skills": [],
            "missing_skills": job_skills if job_skills else [],
            "extra_skills": candidate_skills if candidate_skills else []
        }
    
    try:
        # Generate embeddings with input validation
        job_skills = [str(skill) for skill in job_skills if str(skill).strip()]
        candidate_skills = [str(skill) for skill in candidate_skills if str(skill).strip()]
        
        if not job_skills or not candidate_skills:
            return {
                "matched_skills": [],
                "missing_skills": job_skills,
                "extra_skills": candidate_skills
            }

        # Generate embeddings (batch processing)
        job_skill_embeddings = embedding_model.encode(job_skills, convert_to_tensor=True)
        candidate_skill_embeddings = embedding_model.encode(candidate_skills, convert_to_tensor=True)

        # Ensure we have valid embeddings
        if job_skill_embeddings.shape[0] == 0 or candidate_skill_embeddings.shape[0] == 0:
            return {
                "matched_skills": [],
                "missing_skills": job_skills,
                "extra_skills": candidate_skills
            }

        # Compute cosine similarity matrix
        similarity_matrix = cosine_similarity(
            job_skill_embeddings.cpu().numpy().reshape(len(job_skills), -1),
            candidate_skill_embeddings.cpu().numpy().reshape(len(candidate_skills), -1)
        )

        # Find matched, missing, and extra skills
        matched_skills = []
        missing_skills = []
        extra_skills = candidate_skills.copy()

        for i, job_skill in enumerate(job_skills):
            if similarity_matrix.shape[1] == 0:  # No candidate skills to compare
                missing_skills.append(job_skill)
                continue
                
            max_similarity = np.max(similarity_matrix[i])
            if max_similarity >= threshold:
                matched_index = np.argmax(similarity_matrix[i])
                matched_skill = candidate_skills[matched_index]
                matched_skills.append((job_skill, matched_skill, float(max_similarity)))
                if matched_skill in extra_skills:
                    extra_skills.remove(matched_skill)
            else:
                missing_skills.append(job_skill)

        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extra_skills": extra_skills
        }
        
    except Exception as e:
        print(f"Error in skill comparison: {str(e)}")
        return {
            "matched_skills": [],
            "missing_skills": job_skills,
            "extra_skills": candidate_skills
        }