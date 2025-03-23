import time
from scripts.pinecone_setup import embedding_model

def get_cv_embedding(cv_data, retries=3, timeout=10):
    """
    Convert structured CV data or a list of skills into a meaningful text representation
    and generate embeddings with retry logic.

    Parameters:
        cv_data (dict or list): Parsed CV data (dictionary) or list of skills.
        retries (int): Number of retry attempts for API failures.
        timeout (int): Maximum time (in seconds) to spend on retries.

    Returns:
        tensor: Embedding tensor or None if failed.
    """
    if isinstance(cv_data, dict):
        # If input is a dictionary, generate text representation
        name = cv_data.get("name", "Unknown")
        education = cv_data.get("education", [])
        work_experience = cv_data.get("work_experience", [])
        skills = cv_data.get("skills", [])
        job_title = cv_data.get("job_title", "Unknown")
        latest_school = cv_data.get("latest_school", "Unknown")
        desired_role = cv_data.get("desired_role", "Unknown")

        # Generate text representation for education
        education_text = ", ".join([
            f"{edu.get('degree', 'Unknown Degree')} from {edu.get('institution', 'Unknown Institution')}"
            for edu in education
        ])

        # Generate text representation for work experience
        work_experience_text = ", ".join([
            f"{job.get('role', 'Unknown Role')} at {job.get('company', 'Unknown Company')}"
            for job in work_experience
        ])

        # Generate text representation for skills
        skills_text = ", ".join(skills)

        # Combine all fields into a single text representation
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
        # If input is a list of skills, generate text representation
        text_representation = f"Skills: {', '.join(cv_data)}"
    else:
        raise ValueError("Input must be a dictionary or a list of skills.")

    # Retry logic for generating embeddings
    start_time = time.time()
    for attempt in range(retries):
        try:
            embedding = embedding_model.encode(text_representation, convert_to_tensor=True)
            return embedding
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1 and (time.time() - start_time) < timeout:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Failed to generate embedding after retries.")
                return None