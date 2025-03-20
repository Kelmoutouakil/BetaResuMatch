from django.contrib import admin
from django.urls import path
from .views import CreateUser ,PostFile, GetCrftoken ,  pdfinput, Postregister

urlpatterns = [
    path('create/', CreateUser,name='createUser'),
    # path('login/', Login,name='login'),
    path('render/', PostFile,name='postfile'),
    path('pdf/', pdfinput,name='pdfinput'),
    path('renderregister/', Postregister,name='postregister'),
    path('getcsrf/', GetCrftoken,name='CRftoken'),
]