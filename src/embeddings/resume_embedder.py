import time
from scripts.pinecone_setup import embedding_model

def get_cv_embedding(cv_data, retries=3):
    """
    Convert structured CV data into text representation and generate embeddings with retry logic.
    
    Parameters:
        cv_data (dict): Parsed CV data.
        retries (int): Number of retry attempts for API failures.
    
    Returns:
        tensor: Embedding tensor or None if failed.
    """
    text_representation = f"""
    Name: {cv_data['personal_information'].get('name', 'Unknown')}
    Contact: {cv_data['personal_information'].get('contact_details', 'N/A')}
    Employment Type: {cv_data.get('employment_type', 'N/A')}
    Education: {', '.join([edu['degree'] + ' from ' + edu['institution'] for edu in cv_data.get('education', [])])}
    Work Experience: {', '.join([job['role'] + ' at ' + job['company'] for job in cv_data.get('work_experience', [])])}
    Skills: {', '.join(cv_data.get('skills', []))}
    """

    for attempt in range(retries):
        try:
            # Generate embedding
            return embedding_model.encode(text_representation, convert_to_tensor=True)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s...
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Failed to generate embedding after retries.")
                return None
