from rest_framework import serializers                    # type: ignore
from .models import User, UploadedFile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'mobile', 'otp']

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'table_name', 'file', 'uploaded_at']
