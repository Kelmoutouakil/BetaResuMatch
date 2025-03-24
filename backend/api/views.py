from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializer import ResumeSerializer, ResumeDetailSerializer
from .utils import (
    extract_text, 
    Parse_resume, store_cv_embedding, get_cv_embedding, summarize_text, compare_skill_embeddings,
    rank_candidates, parse_job_description, get_jd_embedding, store_jd_embedding, clear_pinecone
)
from .utils2 import match_resume_to_jd
from users.models import Resume
from rest_framework.permissions import IsAuthenticated
import uuid,os,json


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Upload(request):
    if request.FILES.get('files'):
        uploaded_files = request.FILES.getlist('files')
        for file in uploaded_files:
            print("-----------",file.name,flush=True)
            filename, ext = os.path.splitext(file.name)
            if ext.lower() != '.pdf':
                return JsonResponse({'error': f'Invalid file type: {ext}'}, status=400)
            resume = Resume(user=request.user,file=file)
            resume.file.name = f"{filename}{ext}"
            resume.save()
            text =  extract_text(resume.file.path)
            summary = summarize_text(text)
            parsed_resume = Parse_resume(text)
            print("parsed --",parsed_resume,flush=True)
            resume.parsed_resume = parsed_resume
            resume.name = parsed_resume.get('name')  
            resume.jobtitle = parsed_resume.get('job_title')
            resume.Instutut_name = parsed_resume.get('latest_school')
            resume.desired_role  = parsed_resume.get('desired_role')
            resume.summary = summary
            resume.ExtractSkills = parsed_resume.get('skills')
            resume.save()
            print(" name :  ------",resume.name,"<\n",flush=True)
            print(" jobtitle :  ------",resume.jobtitle,"<\n",flush=True)
            print(" INStutut :  ------",resume.Instutut_name,"<\n",flush=True)
            print(" role :  ------",resume.desired_role,"<\n",flush=True)
            print(" sumarry :  ------",resume.summary,"\n",flush=True)
        return JsonResponse({'status':'File uploaded successefuly'},status=200)
    return JsonResponse({'error': 'No file uploaded'}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def JDupload(request):
    data = json.loads(request.body)
    user =  request.user
    if not data.get('job_description'):
        return JsonResponse({'error':'job describtion not uploaded'}, status=400)
    resumes = Resume.objects.filter(user_id=user.id)
    if not resumes:
        return JsonResponse({'error':'No resumes uploaded!'}, status=404)
    parsed_job_des=parse_job_description(data.get('job_description'))
    jd_skills = parsed_job_des.get("required_skills", [])
    if data.get('model'):
            if data.get('model')== '1':
                for resume in resumes:
                    text =  extract_text(resume.file.path)
                    # parsed_resume = Parse_resume(text)
                    skill_comparison_result = compare_skill_embeddings(jd_skills,  resume.parsed_resume.get("skills", []), threshold=0.8)
                    resume.MatchedSkills = skill_comparison_result["matched_skills"]
                    resume.MissingSkills = skill_comparison_result["missing_skills"]
                    resume.ExtractSkills = skill_comparison_result["extra_skills"]
                    resume.save()
                    score = match_resume_to_jd(text,data.get('job_description'))
                    print("score is ---",score," name : ",resume.file.path,flush=True)
                    print("score ",score, "path ",resume.file.path, flush=True)
                    resume.score = score
                    resume.save()
                ranked_resumes = resumes.order_by('-score')
                serializer = ResumeSerializer(ranked_resumes, many=True)
                return Response(serializer.data)
            elif data.get('model') == '2':
                clear_pinecone()
                try:
                    for resume in resumes:
                        # text =  extract_text(resume.file.path)
                        # parsed_resume = Parse_resume(text)
                        skill_comparison_result = compare_skill_embeddings(jd_skills,  resume.parsed_resume.get("skills", []), threshold=0.8)
                        resume.MatchedSkills = skill_comparison_result["matched_skills"]
                        resume.MissingSkills = skill_comparison_result["missing_skills"]
                        resume.ExtractSkills = skill_comparison_result["extra_skills"]
                        resume.save()
                        resume_id = str(resume.id)
                        resume_embedding = get_cv_embedding(parsed_resume)
                        if resume_embedding is not None:
                            store_cv_embedding(resume_id, resume_embedding)
                except Exception as e:
                    print(f"Error processing resume: {e}",flush=True)
                jd_embedding=get_jd_embedding(parsed_job_des) 
                job_id = "ML engineer"
                store_jd_embedding(job_id, jd_embedding)
                rank_candidates(jd_embedding, exclude_id=job_id, n=resumes.count())
                ranked_resumes = resumes.order_by('-score')
                serializer = ResumeSerializer(ranked_resumes, many=True)
                return Response(serializer.data)
    else:
        return JsonResponse({'error': 'send model'})




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_resume_detail(request):
    try:
        resume = Resume.objects.filter(user_id=request.user.id)
        serializer = ResumeDetailSerializer(resume)
        return Response(serializer.data)
    
    except Resume.DoesNotExist:
        return Response({"detail": "Resume not found."}, status=404)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def filter_resumes_by_extract_skills(request):
    skill = request.query_params.get('skill', None)  
    resumes = Resume.objects.filter(user_id=request.user.id)
    
    if skill:
        resumes = resumes.filter(ExtractSkills__icontains=skill)  
    serializer = ResumeSerializer(resumes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def filter_resumes_by_jobtitle(request):
    jobtitle = request.query_params.get('jobtitle', None)  
    resumes = Resume.objects.filter(user_id=request.user.id)
    
    if jobtitle:
        resumes = resumes.filter(jobtitle__icontains=jobtitle)  
    serializer = ResumeSerializer(resumes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_resume_score(request):
    name = request.data.get('name', None)
    file = request.data.get('file', None)
    score = request.data.get('score', None)

    if not score or (not name and not file):
        return Response({"detail": "Please provide a score and either a name or file."}, status=404)
    try:
        if name:
            resume = Resume.objects.get(user_id=request.user.id, name=name)
        elif file:
            resume = Resume.objects.get(user_id=request.user.id, file=file)
        else:
            return Response({"detail": "No resume found matching provided parameters."}, status=404)
        resume.score = score
        resume.save()
        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

    except Resume.DoesNotExist:
        return Response({"detail": "Resume not found."}, status=404)

    
