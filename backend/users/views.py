from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated
from .forms import UserRegistationForm
import json
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
def CreateUser(request):
    print("request :",request.body,flush=True)
    form = UserRegistationForm(json.loads(request.body))
    if form.is_valid():
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "User already exists with this email."}, status=400)
        user =  User.objects.create_user(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password=password
        )
        user.save()
        return JsonResponse({"data" : "user created"})
    return JsonResponse({"error": form.errors}, status=400)

def PostFile(request):
    return render(request,'login.html')
def pdfinput(request):
    # return render(request,'pdfinput.html')
    return render(request,'jd.html')
def Postregister(request):
    return render(request,'register.html')
@api_view(['Get'])
@permission_classes([IsAuthenticated])
def getuser(request):
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        return JsonResponse({"first_name": first_name, "last_name": last_name})
    return JsonResponse({"error": "User not authenticated"}, status=401)


@api_view(['GET'])
def GetCrftoken(request):
    csrf_token =  get_token(request)
    return JsonResponse({'crfToken': csrf_token})

