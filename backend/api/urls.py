from django.urls import path
from .views import Upload, JDupload,geDashbord, getCandidat ,get_resume_detail, getRankedCandidat, update_feedback, update_resume_score

urlpatterns = [
    path('upload/', Upload, name='upload'), 
    path('JDupload/', JDupload, name='JDupload'),
    path('Details/',get_resume_detail, name='resume_detail'), 
    path('dashbord/', geDashbord, name='dashbord'), 
    path('Rank/',getRankedCandidat, name='RankedCandidates'), 
    path('update/',update_resume_score, name='updatescore'), 
    path('getcandidat/',getCandidat, name='getcandidat'), 
    path('feedback/',update_feedback, name='feedback'), 

    # Make sure the URL pattern is correct
]

