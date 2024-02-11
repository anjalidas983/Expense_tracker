from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password as generic_pwd_validation
from django.core.validators import validate_email as validate_email_format
from . models import CustomUser




class UserRegistrationSerializer(serializers.ModelSerializer):
    def validate_email(self,value):
        try:
            validate_email_format(value)     
        except ValidationError:
            raise serializers.ValidationError('Invalid email format.')    
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already in use.')
        return value



    def validate_password(self,value):
        
        special_char = "@!=_;:.,%$^&*+-?\/><()[]~"
        if not any(char in special_char for char in value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("The password must contain at least one uppercase letter.")
        if len(value)<8:
            raise serializers.ValidationError("Password must contain atleast 8 character.")
        return value
   
    class Meta:
        model=CustomUser
        fields=('id','username','email','password')
       

   
   


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        user = CustomUser.objects.filter(email=value)
        if not user:
            raise serializers.ValidationError('No user found with this email address.')
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        
        special_char = "@!=_;:.,%$^&*+-?\/><()[]~"
        if data['password'] != data['confirm_password']:
            
            raise serializers.ValidationError("Passwords do not match.")
        if not any(char in special_char for char in data['password']):
            raise serializers.ValidationError("Password must contain at least one special character.")
            
        if not any(char.isupper() for char in data['password']):
            raise serializers.ValidationError("The password must contain at least one uppercase letter.")
            
        if len(data['password'])<8:
            raise serializers.ValidationError("Password must contain atleast 8 character.")
           
        return data
