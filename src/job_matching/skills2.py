from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scripts.pinecone_setup import embedding_model

#second approach
def extract_skill_embeddings(skill_names, text_embeddings, skill_to_index):
    """
    Extract embeddings for specific skills from the full text embeddings.

    Parameters:
        skill_names (list): List of skill names.
        text_embeddings (np.array): Embeddings for the full text.
        skill_to_index (dict): Mapping of skill names to their positions in the text.

    Returns:
        np.array: Embeddings for the specified skills.
    """
    skill_indices = [skill_to_index[skill] for skill in skill_names]
    return text_embeddings[skill_indices]

def compare_skill_embeddings(job_skills, candidate_skills, threshold=0.8):
    """
    Compare job skills and candidate skills using embeddings.

    Parameters:
        job_skills (list): List of job skill names.
        candidate_skills (list): List of candidate skill names.
        threshold (float): Similarity threshold for matching skills.

    Returns:
        dict: A dictionary containing matched, missing, and extra skills.
    """
    # Generate embeddings for job skills (batch processing)
    job_skill_embeddings = embedding_model.encode(job_skills, convert_to_tensor=True)

    # Generate embeddings for candidate skills (batch processing)
    candidate_skill_embeddings = embedding_model.encode(candidate_skills, convert_to_tensor=True)

    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(job_skill_embeddings.cpu().numpy(), candidate_skill_embeddings.cpu().numpy())

    # Find matched, missing, and extra skills
    matched_skills = []
    missing_skills = []
    extra_skills = candidate_skills.copy()

    for i, job_skill in enumerate(job_skills):
        max_similarity = np.max(similarity_matrix[i])
        if max_similarity >= threshold:
            matched_index = np.argmax(similarity_matrix[i])
            matched_skill = candidate_skills[matched_index]
            matched_skills.append((job_skill, matched_skill))
            extra_skills.remove(matched_skill)
        else:
            missing_skills.append(job_skill)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills
    }