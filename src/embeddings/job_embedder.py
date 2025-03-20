from scripts.pinecone_setup import embedding_model
def get_jd_embedding(jd_data):
    """
    Convert structured job description data into a meaningful text representation
    and generate embeddings.
    """
    text_representation = f"""
    Job Title: {jd_data.get('job_title', 'Unknown')}
    Employment Type: {jd_data.get('employment_type', 'N/A')}
    Experience Level: {jd_data.get('experience_level', 'N/A')}
    Required Skills: {', '.join(jd_data.get('required_skills', []))}
    Responsibilities: {', '.join(jd_data.get('responsibilities', []))}
    Qualifications: {', '.join(jd_data.get('qualifications', []))}
    """
    return embedding_model.encode(text_representation, convert_to_tensor=True)