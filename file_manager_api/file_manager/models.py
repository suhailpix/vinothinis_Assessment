from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField()
    mime_type = models.CharField(max_length=100)
    permissions = models.ManyToManyField(User, related_name='file_permissions', blank=True)

class FileVersion(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    version = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='files/')

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
