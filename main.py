
import uuid
import time

from src.text_extraction.extractor import extract_text
from src.parser.resume_parser import parse_cv
from src.parser.job_parser import parse_job_description
from src.embeddings.resume_embedder import get_cv_embedding
from src.embeddings.job_embedder import get_jd_embedding
from src.job_matching.matcher import rank_candidates
from src.embeddings.storing import store_cv_embedding, store_jd_embedding

def main():
    resume_paths = [
        r"C:\Users\hp\Downloads\BetaResuMatch\data\ELBACHA_IKRAM_CV__Copy_.pdf",
        r"C:\Users\hp\Downloads\BetaResuMatch\data\rajaa.pdf",
        r"C:\Users\hp\Downloads\BetaResuMatch\data\Yakhou_Yousra___QRT.pdf",
        r"C:\Users\hp\Downloads\BetaResuMatch\data\Zineb-EL-BACHA-BCG.pdf"
    ]

    job_description="""
    We are seeking a Machine Learning Engineer to join our AI research team.
    In this role, you will develop, deploy, and optimize machine learning models 
    to solve real-world problems. You will work closely with data scientists and 
    software engineers to bring AI-driven solutions to production.

    **Responsibilities:**
    - Design, build, and deploy machine learning models.
    - Optimize deep learning and traditional ML algorithms.
    - Preprocess and clean large-scale datasets.
    - Deploy models using MLOps frameworks.

    **Required Skills:**
    - Python, TensorFlow, PyTorch, Scikit-Learn.
    - Experience with data engineering tools (Spark, Kafka, SQL).
    - Familiarity with cloud platforms (AWS, GCP, Azure).
    """
    for resume_path in resume_paths:
        try:
            resume_text = extract_text(resume_path)
            parsed_resume = parse_cv(resume_text)

            resume_id = str(uuid.uuid4())
        
            resume_embedding = get_cv_embedding(parsed_resume)  # Updated function
            if resume_embedding is not None:
                store_cv_embedding(resume_id, resume_embedding)
            else:
                print(f"Failed to embed resume: {resume_path}")

            time.sleep(1)  # Prevent rate limits

        except Exception as e:
            print(f"Error processing resume {resume_path}: {e}")
    


    parsed_job_des=parse_job_description(job_description)
    jd_embedding=get_jd_embedding(parsed_job_des)# why str?the fct get_embeddings expects a string as input
    job_id = "ML_Engineer_Job"  # used a fixed string but can be an id as well
    store_jd_embedding(job_id, jd_embedding)
    #matching and ranking
    ranked_candidates = rank_candidates(jd_embedding)

    if ranked_candidates:
        for rank, candidate in enumerate(ranked_candidates, start=1):
            # Display only the first 8 characters of the UUID for readability
            candidate_id_short = candidate['candidate_id'][:8]
            similarity_score = candidate['similarity_score']
            print(f"Rank {rank}: Candidate ID {candidate_id_short} - Similarity: {similarity_score}")
    else:
        print("No matching candidates found.")

if __name__ == "__main__":
    main()