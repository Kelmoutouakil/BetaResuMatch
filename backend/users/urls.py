from django.contrib import admin
from django.urls import path
from .views import CreateUser , GetCrftoken , getuser

urlpatterns = [
    path('create/', CreateUser,name='createUser'),
    path('getUser/', getuser,name='getuser'),
    path('getcsrf/', GetCrftoken,name='CRftoken'),
]