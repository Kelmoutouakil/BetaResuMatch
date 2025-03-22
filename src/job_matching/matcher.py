from scripts.pinecone_setup import index

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
            top_k=20,
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