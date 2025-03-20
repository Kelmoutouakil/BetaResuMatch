from scripts.pinecone_setup import index

def store_cv_embedding(cv_id, cv_embedding):
    """
    Store candidate embeddings in Pinecone.
    """
    index.upsert([(cv_id, cv_embedding.tolist())])



def store_jd_embedding(jd_id, jd_embedding):       #what about the id here
    """
    Store job description embeddings in Pinecone.
    """
    index.upsert([(jd_id, jd_embedding.tolist())])
