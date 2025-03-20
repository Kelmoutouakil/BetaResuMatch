from django.urls import path
from .views import Upload

urlpatterns = [
    path('upload/', Upload, name='upload'), 
    # Make sure the URL pattern is correct
]

