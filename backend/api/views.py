from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.files.storage import FileSystemStorage
from .utils import extract_text
from .models import Resume
import os
@api_view(['POST'])
def Upload(request):
    if request.FILES.get('file-upload'):
        uploaded_file = request.FILES['file-upload']
        fs = FileSystemStorage()
        file_name = 'latest_resume.pdf'
        file_path = os.path.join(fs.location, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        filename = fs.save(file_name, uploaded_file)
        file_url = fs.url(filename)
        extracted_text = extract_text(file_path)
        print("extracted data : ",extracted_text,flush=True )
        return JsonResponse({'file_url': file_url, 'message': 'File uploaded successfully!'})
    return JsonResponse({'error': 'No file uploaded'}, status=400)
    