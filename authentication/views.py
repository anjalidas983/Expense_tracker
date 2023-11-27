from django.shortcuts import render
from . serializers import UserRegistrationSerializer
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.core.exceptions import ValidationError
from . models import CustomUser
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from .serializers import PasswordResetSerializer,PasswordResetConfirmSerializer
from django.http   import JsonResponse
from rest_framework.generics import get_object_or_404

     
#User registration apiview
class UserRegistrationView(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=UserRegistrationSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        try:
           serializer.is_valid(raise_exception=True)  
        except serializers.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({'message':"User Registerd Successfully."},
                            status=status.HTTP_201_CREATED)
        
#Password reset apiview
class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = get_user_model().objects.filter(email=email).first()

        if user:
      
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = f'http://localhost:3000/confirm-reset-password/{uid}/{token}/'

            subject = 'Password Reset'
            message = f'Hello,\n\nYou have requested to reset your password. Please click on the following link to reset it:\n\n{reset_url}\n\nIf you didn\'t request this, please ignore this email.\n\nThank you'

            send_mail(subject, message, 'anjuzanjali123@gmail.com', [user.email])
        else:
            return Response({'message':'No such user present'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
    

#Password reset confirm apiview
class PasswordResetConfirmView(generics.CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def create(self, request,uidb64,token):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            uid = force_bytes(urlsafe_base64_decode(uidb64)) 
            user = get_object_or_404(get_user_model(), pk=uid)

            if user and default_token_generator.check_token(user, token): 
            
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
            
            else:
                return Response({'error': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            errors = e.detail
            error_response = {'error': 'Invalid data', 'details': errors}
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)