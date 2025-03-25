from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name    = models.CharField(verbose_name="first_name", max_length=20, default='')
    last_name     = models.CharField(verbose_name="last_name", max_length=20, default='')
    email         = models.EmailField(verbose_name="email", unique=True, max_length=60)
    
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    class Meta : 
        db_table = 'user'

    def __str__(self):
        return self.email
    

class Resume(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(null=True, blank=True)
    MatchedSkills=models.TextField(null=True, blank=True)
    feedback=models.TextField(null=True, blank=True)
    MissingSkills=models.TextField(null=True, blank=True)
    ExtractSkills=models.TextField(null=True, blank=True)
    parsed_resume = models.JSONField(default=dict)
    score = models.DecimalField(default=0,max_digits=5, decimal_places=2)
    name = models.CharField(max_length=255, blank=True, null=True)
    jobtitle = models.CharField(max_length=255, blank=True, null=True)
    Instutut_name = models.CharField(max_length=255, blank=True, null=True)
    desired_role = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table= 'resume'
    
    def __str__(self):
        return self.name
 

