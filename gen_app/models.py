from django.db import models
from django import forms

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
