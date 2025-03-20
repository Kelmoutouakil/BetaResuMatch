from scripts.pinecone_setup import index
import uuid

def store_cv_embedding(cv_id, cv_embedding):
    """
    Store candidate embeddings in Pinecone with error handling.
    """
    try:
        index.upsert([(cv_id, cv_embedding.tolist())])
        print(f"Successfully stored CV embedding for ID: {cv_id}")
    except Exception as e:
        print(f"Failed to store CV embedding for ID {cv_id}: {e}")

def store_jd_embedding(jd_id=None, jd_embedding=None):
    """
    Store job description embeddings in Pinecone with error handling.
    If no ID is provided, generate a UUID.
    """
    if jd_id is None:
        jd_id = str(uuid.uuid4())  # Generate a unique ID if not provided
    try:
        index.upsert([(jd_id, jd_embedding.tolist())])
        print(f"Successfully stored JD embedding for ID: {jd_id}")
    except Exception as e:
        print(f"Failed to store JD embedding for ID {jd_id}: {e}")