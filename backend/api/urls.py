from django.urls import path
from .views import Upload, JDupload,  get_resume_detail, filter_resumes_by_extract_skills, update_resume_score

urlpatterns = [
    path('upload/', Upload, name='upload'), 
    path('JDupload/', JDupload, name='JDupload'),
    path('Details/',get_resume_detail, name='resume_detail'), 
    path('filter/',filter_resumes_by_extract_skills, name='filterskils'), 
    path('update/',update_resume_score, name='updatescore'), 

    # Make sure the URL pattern is correct
]

