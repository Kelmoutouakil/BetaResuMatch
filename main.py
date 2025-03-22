import uuid
#import time
 
from src.text_extraction.extractor import extract_text
from src.parser.resume_parser import parse_cv
from src.parser.job_parser import parse_job_description
from src.embeddings.resume_embedder import get_cv_embedding
from src.embeddings.job_embedder import get_jd_embedding
#from src.job_matching.matcher import rank_candidates
from src.embeddings.storing import store_cv_embedding, store_jd_embedding
from scripts.clear_pinecone import clear_pinecone_index
from src.job_matching.skills2 import compare_skill_embeddings


def main():
    clear_pinecone_index()
    resume_paths = [
        r"C:\Users\hp\Downloads\BetaResuMatch\data\Yakhou_Yousra___QRT.pdf",
        r"C:\Users\hp\Downloads\BetaResuMatch\data\Zineb-EL-BACHA-BCG.pdf",
        r"C:\Users\hp\Downloads\BetaResuMatch\data\ELBACHA_IKRAM_CV__Copy_.pdf"
    ]
    job_description = """
    We are seeking a Machine Learning Engineer to join our AI research team.
    In this role, you will develop, deploy, and optimize machine learning models 
    to solve real-world problems.
 
    **Responsibilities:**
    - Design, build, and deploy machine learning models.
    - Optimize deep learning and traditional ML algorithms.
    - Preprocess and clean large-scale datasets.
    - Deploy models using MLOps frameworks.
 
    **Required Skills:**
    - Python, TensorFlow, PyTorch, Scikit-Learn.
    - Experience with data engineering tools (Apache Spark, Apache Kafka, SQL).
    - Cloud Computing, Machine Learning, Deep Learning, Data Engineering, NoSQL, Data Analysis, Data visualization 
    """

    # Parse job description and extract skills
    parsed_job_des = parse_job_description(job_description)
    jd_skills = parsed_job_des.get("required_skills", [])
    print("Job Description Skills:", jd_skills)

    # Process resumes
    for resume_path in resume_paths:
        try:
            # Extract and parse resume text
            resume_text = extract_text(resume_path)
            parsed_resume = parse_cv(resume_text)
            # Ensure parsed_resume is a dictionary and contains a 'skills' key
            if not isinstance(parsed_resume, dict) or "skills" not in parsed_resume:
                print(f"Invalid resume format: {resume_path}")
                continue
            cv_skills = parsed_resume.get("skills", [])

            if jd_skills and cv_skills:
                skill_comparison_result = compare_skill_embeddings(jd_skills, cv_skills, threshold=0.8)
                print(f"\nSkill Comparison for Resume: {resume_path}")
                print("Matched Skills:", skill_comparison_result["matched_skills"])
                print("Missing Skills:", skill_comparison_result["missing_skills"])
                print("Extra Skills:", skill_comparison_result["extra_skills"])
            else:
                print(f"\nNo skills found in job description or resume: {resume_path}")

            # Generate and store CV embedding
            resume_id = str(uuid.uuid4())
            resume_embedding = get_cv_embedding(parsed_resume)
            if resume_embedding is not None:
                store_cv_embedding(resume_id, resume_embedding)
            else:
                print(f"Failed to embed resume: {resume_path}")

        except Exception as e:
            print(f"Error processing resume {resume_path}: {e}")

    # Parse job description and store its embedding
    parsed_job_des = parse_job_description(job_description)
    jd_embedding = get_jd_embedding(parsed_job_des)
    job_id = "ML_Engineer_Job"
    store_jd_embedding(job_id, jd_embedding)

if __name__ == "__main__":
    main()