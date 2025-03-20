from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def parse_job_description(jd_text):
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Gemini API key is not set.")

    prompt = f"""
    Extract the following structured information from the job description below and return a valid JSON object:
    
    {{
        "job_title": "Job title mentioned in the description",
        "employment_type": "Full-time, Part-time, Contract, Internship, etc.",
        "education_requirements": "Required education"
        "description": "Overall job description",
        "experience_level": "Entry-level, Mid-level, Senior, etc.",
        "required_skills": ["Skill1", "Skill2", "Skill3"],
        "responsibilities": [
            "Responsibility 1",
            "Responsibility 2"
        ],
        "qualifications": [
            "Qualification 1",
            "Qualification 2"
        ]
    }}

    Only return JSON. Do not include explanations or text outside this JSON.

    Job Description Text:
    {jd_text}
    """

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    cleaned_text = re.sub(r"```json|```", "", response.text).strip()

    try:
        parsed_job= json.loads(cleaned_text)
    except json.JSONDecodeError:
        print("API returned invalid JSON. Check response format.")
        parsed_job = {"error": "Invalid API response", "raw_response": cleaned_text}

    return parsed_job
