from django.urls import path
from .views import Upload, JDupload,geDashbord, getCandidat ,get_resume_detail,update_feedback, update_resume_score

urlpatterns = [
    path('upload/', Upload, name='upload'), 
    path('JDupload/', JDupload, name='JDupload'),
    path('Details/',get_resume_detail, name='resume_detail'), 
    path('dashbord/', geDashbord, name='dashbord'), 
    # path('filter/',filter_resumes_by_extract_skills, name='filterskils'), 
    # path('filterJob/',filter_resumes_by_jobtitle, name='filterjob'), 
    path('update/',update_resume_score, name='updatescore'), 
    path('getcandidat/',getCandidat, name='getcandidat'), 
    path('feedback/',update_feedback, name='feedback'), 

    # Make sure the URL pattern is correct
]

