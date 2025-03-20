from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import re
import time

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def parse_job_description(jd_text, retries=3):
    """
    Parse a job description into structured JSON format using the Gemini API.
    Implements retry logic with exponential backoff to handle rate limits.

    Parameters:
        jd_text (str): The job description text to parse.
        retries (int): Number of retry attempts for API failures.

    Returns:
        dict: Parsed job description as a dictionary or an error dictionary.
    """
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
        "required_skills": ["Skill1", "Skill2", "Skill3"]
    }}

    Only return JSON. Do not include explanations or text outside this JSON.

    Job Description Text:
    {jd_text}
    """

    model = genai.GenerativeModel("gemini-1.5-pro")

    for attempt in range(retries):
        try:
            # Generate response from Gemini API
            response = model.generate_content(prompt)
            cleaned_text = re.sub(r"```json|```", "", response.text).strip()

            # Parse the cleaned text into JSON
            parsed_job = json.loads(cleaned_text)
            return parsed_job

        except json.JSONDecodeError:
            print(f"Attempt {attempt + 1}: API returned invalid JSON. Retrying...")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Failed to parse job description after retries.")
                return {"error": "Invalid API response", "raw_response": cleaned_text}

        except Exception as e:
            print(f"Attempt {attempt + 1}: Error parsing job description - {e}")
            if attempt < retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Waiting for {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Failed to parse job description after retries.")
                return {"error": str(e), "raw_response": response.text if 'response' in locals() else None}

    return {"error": "All retry attempts failed", "raw_response": None}