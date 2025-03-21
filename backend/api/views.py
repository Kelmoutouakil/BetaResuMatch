from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from .utils import (
    extract_text, Parse_resume, rank_candidates, store_cv_embedding, 
    parse_job_description, get_jd_embedding, store_jd_embedding, get_cv_embedding
)
from .models import Resume
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.permissions import IsAuthenticated
import uuid,os,json
ALLOWED_EXTENSIONS = {'.pdf', '.png'}
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Upload(request):
   
    if request.FILES.get('files[]'):
        uploaded_files = request.FILES.getlist('files[]')
        saved_files = []
        for file in uploaded_files:
            filename, ext = os.path.splitext(file.name)
            if ext.lower() not in ALLOWED_EXTENSIONS:
                return JsonResponse({'error': f'Invalid file type: {ext}'}, status=400)
            resume = Resume(user=request.user)
            resume.save()
            candidat_id = resume.id
            new_filename = f"{filename}_{candidat_id}{ext}"
            saved_path = default_storage.save(new_filename, ContentFile(file.read()))
            full_file_path =  default_storage.path(saved_path)
            
            resume.file = full_file_path
            resume.save()
            saved_files.append({
                'file_name': new_filename,
                'file_path': full_file_path
            })  
        return JsonResponse({'status':'success'})
    return JsonResponse({'error': 'No file uploaded'}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def JDupload(request):
    data = json.loads(request.body)
    user =  request.user
    if not data.get('job_description'):
        return JsonResponse({'error':'job describtion not uploaded'}, status=400)
    print("-----------user-------------",user, flush=True)
    try:
        resumes = Resume.objects.filter(user=user)
        print("Number of resumes fetched:", resumes.count(), flush=True)  
        for resume in resumes:
            parsed_resume = Parse_resume(extract_text(resume.file.path))
            print(".....", parsed_resume, flush=True)  
            resume.name = parsed_resume.get('name')  
            resume.save()
            resume_id = str(uuid.uuid4())
            resume_embedding = get_cv_embedding(parsed_resume)
            if resume_embedding is not None:
                store_cv_embedding(resume_id, resume_embedding)
            else:
                print(f"Failed to embed resume: {resume.file.path}")
            print("data : ", parsed_resume.get('name') , flush=True)    
    except Exception as e:
            print(f"Error processing resume: {e}")
    print("------------------------", flush=True)
    parsed_job_des=parse_job_description(data.get('job_description'))
    jd_embedding=get_jd_embedding(parsed_job_des)
    job_id = "ML_Engineer_Job" 
    store_jd_embedding(job_id, jd_embedding)
    ranked_candidates = rank_candidates(jd_embedding, exclude_id=job_id) 
    print("ranked :",ranked_candidates, flush=True)
    return JsonResponse({'status':'success'})