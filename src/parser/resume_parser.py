from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def parse_cv(cv_text):
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Gemini API key is not set.")

    prompt = f"""
        Extract the following information from the CV below and return a valid JSON object:
    
    {{
        "personal_information": {{
            "name": "Full name",
            "contact_details": "Email, phone number, and other available contacts"
        }},
        "employment_type": "Full-time, Part-time, Contract, Internship, etc.",
        "education": [
            {{
                "degree": "Degree title",
                "institution": "University or school name",
                "year": "Year of completion"
            }}
        ],
        "work_experience": [
            {{
                "company": "Company name",
                "role": "Job title",
                "duration": "Start and end dates",
                "projects": "Key projects and contributions"
            }}
        ],
        "skills": ["Skill1", "Skill2", "Skill3"]
    }}

    Only return JSON. Do not include explanations or text outside this JSON.

    

    CV Text:
    {cv_text}
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    cleaned_text = re.sub(r"```json|```", "", response.text).strip()

    try:
        parsed_info = json.loads(cleaned_text)
    except json.JSONDecodeError:
        print("API returned invalid JSON. Check response format.")
        parsed_info = {"error": "Invalid API response", "raw_response": cleaned_text}
    

    return parsed_info
