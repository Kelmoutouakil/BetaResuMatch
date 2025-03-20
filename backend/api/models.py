from django.db import models

class Resume(models.Model):
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    job_name = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table= 'resume'
    
    def __str__(self):
        return self.file_name
