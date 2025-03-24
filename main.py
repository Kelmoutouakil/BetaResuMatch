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
from src.job_matching.skills2 import compare_skill_embeddings

def main():
    clear_pinecone_index()
    resume_path = r"C:\Users\hp\Downloads\BetaResuMatch\data\Zineb-EL-BACHA-BCG.pdf"
    job_description = """
    Backen developer
    """
    jd_data = parse_job_description(job_description)
    resume_text=extract_text(resume_path)
    resume_data = parse_cv(resume_text)
    jd_skills = jd_data.get("required_skills", [])
    resume_skills = resume_data.get("skills", [])
    comparison_result = compare_skill_embeddings(jd_skills, resume_skills)
    print(comparison_result)

    


if __name__ == "__main__":
    main()