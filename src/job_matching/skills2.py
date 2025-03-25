#Second approach; similarity search
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scripts.pinecone_setup import embedding_model

def compare_skill_embeddings(job_skills, candidate_skills, threshold=0.8):
    """
    Compare job skills and candidate skills using embeddings with robust error handling.

    Parameters:
        job_skills (list): List of job skill names.
        candidate_skills (list): List of candidate skill names.
        threshold (float): Similarity threshold for matching skills.

    Returns:
        dict: A dictionary containing matched, missing, and extra skills.
    """
    # Handle empty inputs
    if not job_skills or not candidate_skills:
        return {
            "matched_skills": [],
            "missing_skills": job_skills if job_skills else [],
            "extra_skills": candidate_skills if candidate_skills else []
        }
    
    try:
        # Generate embeddings with input validation
        job_skills = [str(skill) for skill in job_skills if str(skill).strip()]
        candidate_skills = [str(skill) for skill in candidate_skills if str(skill).strip()]
        
        if not job_skills or not candidate_skills:
            return {
                "matched_skills": [],
                "missing_skills": job_skills,
                "extra_skills": candidate_skills
            }

        # Generate embeddings (batch processing)
        job_skill_embeddings = embedding_model.encode(job_skills, convert_to_tensor=True)
        candidate_skill_embeddings = embedding_model.encode(candidate_skills, convert_to_tensor=True)

        # Ensure we have valid embeddings
        if job_skill_embeddings.shape[0] == 0 or candidate_skill_embeddings.shape[0] == 0:
            return {
                "matched_skills": [],
                "missing_skills": job_skills,
                "extra_skills": candidate_skills
            }

        # Compute cosine similarity matrix
        similarity_matrix = cosine_similarity(
            job_skill_embeddings.cpu().numpy().reshape(len(job_skills), -1),
            candidate_skill_embeddings.cpu().numpy().reshape(len(candidate_skills), -1)
        )

        # Find matched, missing, and extra skills
        matched_skills = []
        missing_skills = []
        extra_skills = candidate_skills.copy()

        for i, job_skill in enumerate(job_skills):
            if similarity_matrix.shape[1] == 0:  # No candidate skills to compare
                missing_skills.append(job_skill)
                continue
                
            max_similarity = np.max(similarity_matrix[i])
            if max_similarity >= threshold:
                matched_index = np.argmax(similarity_matrix[i])
                matched_skill = candidate_skills[matched_index]
                matched_skills.append((job_skill, matched_skill, float(max_similarity)))
                if matched_skill in extra_skills:
                    extra_skills.remove(matched_skill)
            else:
                missing_skills.append(job_skill)

        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "extra_skills": extra_skills
        }
        
    except Exception as e:
        print(f"Error in skill comparison: {str(e)}")
        return {
            "matched_skills": [],
            "missing_skills": job_skills,
            "extra_skills": candidate_skills
        }