from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from .utils import (
    extract_text, Parse_resume, store_cv_embedding, get_cv_embedding, summarize_text, compare_skill_embeddings,
    rank_candidates, parse_job_description, get_jd_embedding, store_jd_embedding, clear_pinecone
)
from users.models import Resume
from rest_framework.permissions import IsAuthenticated
import uuid,os,json


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Upload(request):
    if request.FILES.get('files'):
        uploaded_files = request.FILES.getlist('files')
        saved_files = []
        for file in uploaded_files:
            # print("-----------",file.name,flush=True)
            filename, ext = os.path.splitext(file.name)
            if ext.lower() != '.pdf':
                return JsonResponse({'error': f'Invalid file type: {ext}'}, status=400)
            resume = Resume(user=request.user,file=file)
            resume.file.name = f"{filename}{ext}"
            resume.save()
            saved_files.append({
                'file_name': resume.file.name,
                'file_path': resume.file.path
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
    clear_pinecone()
    try:
        resumes = Resume.objects.filter(user_id=user.id)
        if not resumes:
            return JsonResponse({'error':'No resumes uploaded!'}, status=404)
        parsed_job_des=parse_job_description(data.get('job_description'))
        jd_skills = parsed_job_des.get("required_skills", [])
        for resume in resumes:
            text =  extract_text(resume.file.path)
            summary = summarize_text(text)
            parsed_resume = Parse_resume(text)
            skill_comparison_result = compare_skill_embeddings(jd_skills,  parsed_resume.get("skills", []), threshold=0.8)
            print(f"\nSkill Comparison for Resume:",resume.file.path,flush=True)
            print("Matched Skills:", skill_comparison_result["matched_skills"],flush=True)
            print("Missing Skills:", skill_comparison_result["missing_skills"],flush=True)
            print("Extra Skills:", skill_comparison_result["extra_skills"],flush=True)
            resume.name = parsed_resume.get('name')  
            resume.summary = summary
            resume.MatchedSkills = skill_comparison_result["matched_skills"]
            resume.MissingSkills = skill_comparison_result["missing_skills"]
            resume.ExtractSkills = skill_comparison_result["extra_skills"]
            resume.save()
            resume_id = str(resume.id)
            resume_embedding = get_cv_embedding(parsed_resume)
            if resume_embedding is not None:
                store_cv_embedding(resume_id, resume_embedding)
            else:
                print(f"Failed to embed resume: {resume.file.path}")
    except Exception as e:
            print(f"Error processing resume: {e}",flush=True)
    jd_embedding=get_jd_embedding(parsed_job_des) 
    job_id = "ML_Engineer_Job" 
    store_jd_embedding(job_id, jd_embedding)
    ranked_candidates = rank_candidates(jd_embedding, exclude_id=job_id, n=resumes.count())
    print(ranked_candidates,flush=True)
    if not ranked_candidates :
        return JsonResponse({'status':'no matched resumes with your job description :('})
    
    return JsonResponse({'status':'success'})