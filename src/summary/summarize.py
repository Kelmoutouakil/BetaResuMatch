from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the Mixtral model using InferenceClient
repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
client = InferenceClient(model=repo_id, token=os.getenv('HUGGINGFACE_API_KEY'))

def summarize_text(text):
    """
    Generate a summary of the input text using the Mixtral model.
    """

    prompt = f"""
    Summarize the following text into a concise and complete paragraph. Focus only on:
    - Current role or academic status
    - Educational background
    - Relevant work experience
    - Technical skills and expertise

    Exclude any information about spoken languages, hobbies, or interests. Ensure the summary is well-structured and does not exceed 50 words:
    
    {text}
    """
    response = client.text_generation(prompt)
    return response