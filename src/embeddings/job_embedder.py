from scripts.pinecone_setup import embedding_model
import time
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