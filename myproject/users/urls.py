from django.urls import path                             # type: ignore
from .views import SignupView, LoginView, FileUploadView, UserDetailView
from .views import RequestOTPView,VerifyOTPView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/request-otp/', RequestOTPView.as_view()),  # Request OTP
    path('login/verify-otp/', VerifyOTPView.as_view()),    
    path('upload-file/', FileUploadView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),
]
