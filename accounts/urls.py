from .views import SignUpAPIView, SignInAPIView, ForgotPasswordAPIView, VerifyCodeAPIView, SetNewPasswordAPIView
from django.urls import path

urlpatterns = [
   
    path('api/sign_up/', SignUpAPIView.as_view(), name='sign_up'),
    path('api/sign_in/', SignInAPIView.as_view(), name='sign_in'),
    path('api/forgot_password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('api/verify_code/', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('api/setnew_password/', SetNewPasswordAPIView.as_view(), name='setnew_password'),
]
