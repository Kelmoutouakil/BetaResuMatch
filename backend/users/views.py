from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated
from .forms import UserRegistationForm
import json
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User
from django.contrib.auth import authenticate



@api_view(['POST'])
def CreateUser(request):
    form = UserRegistationForm(json.loads(request.body))
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']

    user =  User.objects.create_user(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password=password
    )
    user.save()
    return JsonResponse({"data" : "user created"})


def PostFile(request):
    return render(request,'login.html')
def pdfinput(request):
    return render(request,'pdfinput.html')
def Postregister(request):
    return render(request,'register.html')

@api_view(['GET'])
def GetCrftoken(request):
    csrf_token =  get_token(request)
    return JsonResponse({'crfToken': csrf_token})

# @api_view(['POST'])
# def Login(request):
#     data =  json.loads(request.body)
#     print("****data*** : ",data,flush=True)
#     if not data.get('email') or not data.get('password'):
#         return JsonResponse({'status':'error', 'message' : 'cridentiel format error'})
#     try:
#         validate_email(data.get('email'))
#     except ValidationError:
#         return JsonResponse({'status': 'error', 'message': 'Invalid email format'})
#     user =  authenticate(request,email=data.get('email'),password=data.get('password'))
#     if not user:
#            return JsonResponse({"status": "error", "message": "Invalid email or password"}, status=400)
#     refresh = RefreshToken.for_user(user)
#     access_token = str(refresh.access_token)
#     access_token.set_exp(lifetime=timedelta(minutes=15))
#     print("payload : ",refresh.access_token.payload,flush=True)
#     refresh_token = str(refresh)
#     return JsonResponse({"status": "success", "message": "Login successful",'access' : access_token,'refresh' : refresh_token})