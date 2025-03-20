import numpy as np
from scripts.pinecone_setup import index

def rank_candidates(jd_embedding):
    """
    Retrieve the top matching candidates from Pinecone and rank them.
    """
    results = index.query(jd_embedding.tolist(), top_k=10, include_values=True)
    
    ranked_candidates = []
    for match in results['matches']:
        similarity_percentage = round(match['score'] * 100, 2)  # Convert score to percentage
        ranked_candidates.append({
            "candidate_id": match['id'],
            "similarity_score": f"{similarity_percentage}%"  # Format as percentage string
        })
    
    return sorted(
        ranked_candidates,
        key=lambda x: float(x["similarity_score"].strip('%')),  # Extract numerical value for sorting
        reverse=True
    )
