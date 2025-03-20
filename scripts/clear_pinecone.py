from scripts.pinecone_setup import index
def clear_pinecone_index():
    """
    Clear all vectors from the Pinecone index.
    """
    try:
        index.delete(delete_all=True)
        print("Pinecone index cleared.")
    except Exception as e:
        print(f"Error clearing Pinecone index: {e}")