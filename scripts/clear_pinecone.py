from scripts.pinecone_setup import index

def clear_pinecone_index(namespace=""):
    """
    Clear all vectors from the Pinecone index in a specific namespace.
    If the namespace is empty, it clears the default namespace.

    Parameters:
        namespace (str): The namespace to clear. Default is an empty string.
    """
    try:
        # Check if the index is empty
        stats = index.describe_index_stats()
        if stats["namespaces"].get(namespace, {}).get("vector_count", 0) == 0:
            print(f"Namespace '{namespace}' is already empty.")
            return

        # Delete all vectors in the specified namespace
        index.delete(delete_all=True, namespace=namespace)
        print(f"Successfully cleared namespace '{namespace}'.")
    except Exception as e:
        print(f"Error clearing Pinecone index: {e}")