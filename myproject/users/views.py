from rest_framework.views import APIView                     # type: ignore
from rest_framework.response import Response               # type: ignore
from rest_framework import status                          # type: ignore
from .models import User, UploadedFile
from .serializers import UserSerializer, UploadedFileSerializer
from django.db import connection                            # type: ignore
import random

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestOTPView(APIView):
    """
    Generate and send OTP to the mobile number for login.
    """
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = str(random.randint(1000, 9999))  # Generate a 4-digit OTP
        try:
            user = User.objects.get(mobile=mobile)
            user.otp = otp
            user.save()
            return Response({"message": "OTP sent successfully", "otp": otp}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Mobile number not found"}, status=status.HTTP_404_NOT_FOUND)


class VerifyOTPView(APIView):
    """
    Verify the OTP provided by the user for login.
    """
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(mobile=mobile, otp=otp)
            user.otp = None  # Clear OTP after successful login
            user.save()
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid OTP or mobile number"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = str(random.randint(1000, 9999))
        try:
            user = User.objects.get(mobile=mobile)
            user.otp = otp
            user.save()
            return Response({"otp": otp}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Mobile number not found"}, status=status.HTTP_404_NOT_FOUND)

class FileUploadView(APIView):
    def post(self, request):
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            file_instance = serializer.save()
            table_name = file_instance.table_name
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    CREATE TABLE {table_name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        data TEXT
                    )
                """)
            return Response({"table_name": table_name}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
