from django.urls import path
from .views import Upload, JDupload

urlpatterns = [
    path('upload/', Upload, name='upload'), 
    path('JDupload/', JDupload, name='JDupload'), 
    # Make sure the URL pattern is correct
]

