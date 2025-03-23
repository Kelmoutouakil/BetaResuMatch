import uuid
import time
from src.text_extraction.extractor import extract_text
from src.parser.resume_parser import parse_cv
from src.parser.job_parser import parse_job_description
from src.embeddings.resume_embedder import get_cv_embedding
from src.embeddings.job_embedder import get_jd_embedding
from src.job_matching.matcher import rank_candidates
from src.embeddings.storing import store_cv_embedding, store_jd_embedding
from scripts.clear_pinecone import clear_pinecone_index

def main():
    clear_pinecone_index()
    resume_paths = [
        r"C:\Users\hp\Downloads\BetaResuMatch\data\ELBACHA_IKRAM_CV__Copy_.pdf",
        r"C:\Users\hp\Downloads\BetaResuMatch\data\Yakhou_Yousra___QRT.pdf",
        r"C:\Users\hp\Downloads\BetaResuMatch\data\black  Resume.pdf",
        r"C:\Users\hp\Downloads\BetaResuMatch\data\rajaa.pdf",
        r"C:\Users\hp\Downloads\BetaResuMatch\data\Zineb-EL-BACHA-BCG.pdf"

    ]
    job_description = """
    Job Title: Machine Learning Engineer
    Required Skills:
    Strong programming skills in Python (TensorFlow, PyTorch, Scikit-learn).
    Experience with machine learning algorithms (supervised, unsupervised, deep learning).
    Proficiency in data preprocessing and feature engineering.
    Knowledge of model deployment (Docker, Flask, FastAPI, or cloud services like AWS, GCP, Azure).
    Experience with MLOps tools (MLflow, Kubeflow, CI/CD for ML).
    Familiarity with big data technologies (Spark, Hadoop) and databases (SQL, NoSQL).
    Strong understanding of statistics, probability, and optimization.
    Experience with vector databases and retrieval-augmented generation (RAG) is a plus.

  
    """

    # Dictionary to map resume_id to resume_path
    resume_id_to_path = {}

    # Store resume embeddings
    for resume_path in resume_paths:
        try:
            resume_text = extract_text(resume_path)
            parsed_resume = parse_cv(resume_text)
 
            resume_id = str(uuid.uuid4())
            resume_id_to_path[resume_id] = resume_path  # Store mapping between resume_id and resume_path
         
            resume_embedding = get_cv_embedding(parsed_resume)  # Updated function
            if resume_embedding is not None:
                store_cv_embedding(resume_id, resume_embedding)  # Store embedding without resume_path
            else:
                print(f"Failed to embed resume: {resume_path}")
 
            time.sleep(3)  # Prevent rate limits
 
        except Exception as e:
            print(f"Error processing resume {resume_path}: {e}")
     
    # Parse job description and store its embedding
    parsed_job_des = parse_job_description(job_description)
    jd_embedding = get_jd_embedding(parsed_job_des)
    job_id = "Mec_Engineer_Job"  # used a fixed string but can be an id as well
    store_jd_embedding(job_id, jd_embedding)

    # Rank candidates
    ranked_candidates = rank_candidates(jd_embedding, exclude_id=job_id)
 
    if ranked_candidates:
        for rank, candidate in enumerate(ranked_candidates, start=1):
            candidate_id_short = candidate['candidate_id'][:8]
            similarity_score = candidate['similarity_score']
            resume_path = resume_id_to_path.get(candidate['candidate_id'], "Unknown")  # Retrieve resume_path from the mapping
            print(f"Rank {rank}: Candidate ID {candidate_id_short} - Similarity: {similarity_score} - Resume Path: {resume_path}")
    else:
        print("No matching candidates found.")


if __name__ == "__main__":
    main()