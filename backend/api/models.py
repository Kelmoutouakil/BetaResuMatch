from django.db import models
from users.models import User

class Resume(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    job_name = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table= 'resume'
    
    def __str__(self):
        return self.name
