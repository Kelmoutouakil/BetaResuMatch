from src.text_extraction.extractor import extract_text
from src.summary.summarize import summarize_text

def main():
    #clear_pinecone_index()
    resume_path=r"C:\Users\hp\Downloads\BetaResuMatch\data\rajaa.pdf"
    cv_text=extract_text(resume_path)
    summary = summarize_text(cv_text)
    print(summary)

if __name__ == "__main__":
    main()