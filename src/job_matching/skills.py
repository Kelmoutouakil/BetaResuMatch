#first approach:
def compare_skills(job_skills, candidate_skills):
    """
    Compare skills between a job description and a candidate profile.

    Parameters:
        job_skills (list): List of skills required by the job description.
        candidate_skills (list): List of skills in the candidate's profile.

    Returns:
        dict: A dictionary containing matched, missing, and extra skills.
    """
    # Convert lists to sets for comparison
    job_skills_set = set(job_skills)
    candidate_skills_set = set(candidate_skills)

    matched_skills = list(job_skills_set.intersection(candidate_skills_set))
    missing_skills = list(job_skills_set - candidate_skills_set)
    extra_skills = list(candidate_skills_set - job_skills_set)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills
    }