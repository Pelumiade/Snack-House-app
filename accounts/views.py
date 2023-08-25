from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignUpSerializer, SignInSerializer, VerifyCodeSerializer, ForgotPasswordSerializer, SetNewPasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
from .tasks import send_email
import random
from .models import User
from rest_framework.generics import CreateAPIView


class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [] 
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Account Succesfully Created'}, status=status.HTTP_201_CREATED)
        

        # Check if the email error exists in the serializer errors
        error_message = serializer.errors.get('email', 'An account with this email already exists.')
        return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    
class SignInAPIView(TokenObtainPairView):
    serializer_class = SignInSerializer
    permission_classes = [] 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
    
        custom_payload = serializer.validated_data
        return Response(custom_payload)
    
        
class ForgotPasswordAPIView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    authentication_classes = ()
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            print(email)
            try:
                user = User.objects.filter(email=email).get()
            except User.DoesNotExist:
                return Response({"error": "Invalid email address. Enter a correct email address"}, status=status.HTTP_400_BAD_REQUEST)

            otp = str(random.randint(1000, 9999))
            print(otp)
            user.verification_code = otp
            user.save(update_fields=["verification_code"])
            # send email
            subject = "Password Reset Verification code"
            body = f'Your verification code is {otp}'
            data = {"email_body": body, "to_email": email,
                    "email_subject": subject}
            send_email(data)
            return Response({'message': 'Verification code sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyCodeAPIView(GenericAPIView):
    serializer_class = VerifyCodeSerializer
    authentication_classes = ()
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        verification_code = serializer.validated_data["verification_code"]
        try:
            user = User.objects.filter(email=email).get()
        except User.DoesNotExist:
            return Response({"message": "Incorrect credential"}, status=status.HTTP_404_NOT_FOUND)
        print(user.verification_code)
        if user.verification_code != verification_code:
            return Response({"message": "Incorrect verification pin."}, status=status.HTTP_400_BAD_REQUEST)
        user.verification_code = ""
        user.save(update_fields=["verification_code"])
        return Response({"message": "verification successful"}, status=status.HTTP_200_OK)


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    authentication_classes = ()
    permission_classes = []

    def post(self, request):
        serilizer = self.get_serializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        email = serilizer.validated_data["email"]
        new_password = serilizer.validated_data["new_password"]
        user = User.objects.filter(email=email).get()
        if user:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)
