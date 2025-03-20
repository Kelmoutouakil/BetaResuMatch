from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils import extract_text
from .models import Resume
from django.core.files.base import ContentFile
import os,json
from django.core.files.storage import default_storage

@api_view(['POST'])
def Upload(request):
   
    if request.FILES.get('files[]'):
        uploaded_files = request.FILES.getlist('files[]')
        saved_files = []
        resume =  Resume()
        resume.save()
        candidat_id = resume.id
        for file in uploaded_files:
            filename, ext = os.path.splitext(file.name)
            new_filename = f"{filename}_{candidat_id}{ext}"
            file_path =new_filename
            saved_path = default_storage.save(file_path, ContentFile(file.read()))
            full_file_path =  default_storage.path(saved_path)
            resume.file = full_file_path
            resume.save()
            saved_files.append({
                'file_name': new_filename,
                'file_path': file_path
            })  
        # extracted_text = extract_text(full_file_path)
        # print("**********************",flush=True)
        # print("extracted data : ",extracted_text,flush=True )
        # print("**********************",flush=True)
   
        return JsonResponse({'status':'success'})
    return JsonResponse({'error': 'No file uploaded'}, status=400)
    
# @api_view(['POST'])
# def JDupload(request):
#     data = json.loads(request.body)
    