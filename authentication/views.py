from django.shortcuts import render
from . serializers import UserRegistrationSerializer
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.core.exceptions import ValidationError
from . models import CustomUser






# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    # permission_classes=(AllowAny,)
    queryset=CustomUser.objects.all()
    serializer_class=UserRegistrationSerializer
    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            validated_data = serializer.validated_data
            username = validated_data.get('username')
            email = validated_data.get('email')
            password = validated_data.get('password')
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.save()
            return Response({'message':"User Registerd Successfully."},
                            status=status.HTTP_201_CREATED)
        else:
            errors=serializer.errors
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)
         



