from django.db import models                           # type: ignore
import random

def generate_table_name():
    return f"table_{random.randint(1000000000, 9999999999)}"

class User(models.Model):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=4, blank=True, null=True)

class UploadedFile(models.Model):
    table_name = models.CharField(max_length=30, default=generate_table_name, unique=True)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
