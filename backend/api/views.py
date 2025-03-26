from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializer import ResumeSerializer, ResumeDetailSerializer
from django.db.models import Count, Case, When, F, Value
from .utils import (
    extract_text, 
    Parse_resume, store_cv_embedding, get_cv_embedding, summarize_text, compare_skill_embeddings,
    rank_candidates, parse_job_description, get_jd_embedding, store_jd_embedding, clear_pinecone
)
from .utils2 import match_resume_to_jd
from users.models import Resume
from rest_framework.permissions import IsAuthenticated
import uuid,os,json
from django.core.files.storage import default_storage

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Upload(request):
    print(" request here ",request.FILES.getlist('files'),flush=True)
    if request.FILES.get('files'):
        uploaded_files = request.FILES.getlist('files')
        for file in uploaded_files:
            print("-----------",file.name,flush=True)
            filename, ext = os.path.splitext(file.name)
            if ext.lower() != '.pdf':
                return JsonResponse({'error': f'Invalid file type: {ext}'}, status=400)
            text = extract_text(file)
            parsed_resume = Parse_resume(text)
            extracted_name = parsed_resume.get('name')
            if not extracted_name:
                return JsonResponse({'error': 'Could not extract name from resume'}, status=400)
            existing_resume = Resume.objects.filter(user=request.user, name=extracted_name).first()
            if existing_resume:
                if existing_resume.file and default_storage.exists(existing_resume.file.path):
                    default_storage.delete(existing_resume.file.path)
                existing_resume.file = file
                existing_resume.summary = summarize_text(text)
                existing_resume.parsed_resume = parsed_resume
                existing_resume.jobtitle = parsed_resume.get('job_title')
                existing_resume.Instutut_name = parsed_resume.get('latest_school')
                existing_resume.desired_role = parsed_resume.get('desired_role')
                existing_resume.ExtractSkills = parsed_resume.get('skills')
                existing_resume.save()
                resume = existing_resume  
            else:
                resume = Resume(
                    user=request.user,
                    file=file,
                    name=extracted_name,
                    summary=summarize_text(text),
                    parsed_resume=parsed_resume,
                    jobtitle=parsed_resume.get('job_title'),
                    Instutut_name=parsed_resume.get('latest_school'),
                    desired_role=parsed_resume.get('desired_role'),
                    ExtractSkills=parsed_resume.get('skills')
                )
                resume.save()
        # serializer = ResumeDetailSerializer(Resume.objects.filter(user_id=request.user.id), many=True)
        # return Response(serializer.data)
        return JsonResponse({'success': ' file uploaded'}, status=200)
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
                    text =  extract_text(resume.file)
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
    

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def filter_resumes_by_extract_skills(request):
#     print("request body ",json.loads(request.body))
#     skill = json.loads(request.body).get('skill') 
#     print("-----------------",skill,flush=True)
#     if skill:
#         resumes = Resume.objects.filter(user_id=request.user.id)
#         for resume in resumes:
#             resume.ExtractSkills = [skil.upper() for skil in resume.ExtractSkills]
#             resume.save() 
#         skill = skill.upper()
#         r=Resume.objects.filter(user_id=request.user.id, ExtractSkills__contains=skill)                           
#         print("RESUMES HERE",skill,flush=True)
#         serializer = ResumeSerializer(r, many=True)
#         print("data ",serializer.data,flush=True)
#         return Response(serializer.data)
#     else:
#         return JsonResponse({"error": 'bad request'},status=400)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def filter_resumes_by_jobtitle(request):
#     try:
#         request_data = json.loads(request.body)
#         print("Request body:", request_data, flush=True)
#         jobtitle = request_data.get('jobtitle')
#         if jobtitle:
#             jobtitle = jobtitle.strip().lower()
#             print(f"Normalized job title being searched: {jobtitle}", flush=True)
#             resumes = Resume.objects.filter(
#                 user_id=request.user.id,
#                 jobtitle__iexact=jobtitle
#             )
#             if resumes.exists():
#                 serializer = ResumeSerializer(resumes, many=True)
#                 print("Serialized data:", serializer.data, flush=True)
#                 return Response(serializer.data)
#             else:
#                 return JsonResponse({"error": "No resumes found matching the job title"}, status=404)
#         else:
#             return JsonResponse({"error": "Job title not provided"}, status=400)

#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCandidat(request):
    serializer = ResumeSerializer(Resume.objects.filter(user_id=request.user.id), many=True)
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_feedback(request):
    name = request.data.get('name', None)
    file = request.data.get('file', None)
    feedback = request.data.get('feedback', None)

    if not feedback or (not name and not file):
        return Response({"detail": "Please provide a feedback and either a name or file."}, status=404)
    try:
        if name:
            resume = Resume.objects.get(user_id=request.user.id, name=name)
        elif file:
            resume = Resume.objects.get(user_id=request.user.id, file=file)
        else:
            return Response({"detail": "No resume found matching provided parameters."}, status=404)
        resume.feedback = feedback
        resume.save()
        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

    except Resume.DoesNotExist:
        return Response({"detail": "Resume not found."}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def geDashbord(request):
    resume = Resume.objects.filter(user_id=request.user.id)

    candidat_count = resume.values('Instutut_name').annotate(resume_count=Count('id')).order_by('Instutut_name')
    job_counts = resume.annotate(
        job_or_role=Case(
            When(jobtitle__isnull=True, then=F('desired_role')), 
            default=F('jobtitle'),  
            output_field=models.CharField()  
        )
    ).values('job_or_role').annotate(resume_count=Count('id')).order_by('job_or_role')
    school_data = {item['Instutut_name']: item['resume_count'] for item in candidat_count}
    job_data = {item['job_or_role']: item['resume_count'] for item in job_counts}
    return JsonResponse({
        'school_data': school_data,
        'job_data': job_data
    })
