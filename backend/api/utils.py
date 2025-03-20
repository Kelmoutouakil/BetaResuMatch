from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from dotenv import load_dotenv
import google.generativeai as genai

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file_path.endswitch(('.png', '.jpg', '.jpeg')):
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    else:
        raise ValueError("Unsupport file format")
 
load_dotenv()  
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def Parse_resume(text):
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Gemini API key is not set.")
    prompt = f"""Extract the following information from the CV below:
    - Personal Information (name, contact details)
    - Education (degree, institution, year)
    - Work Experience (company, role, duration) and projects
    - Skills
    Don't include any other informations.
    
    CV Text:
    {text}
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text