from rest_framework import serializers
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
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
        # value = generic_pwd_validation(value)
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
       

    # def create(self,validated_data):
    #     import pdb;pdb.set_trace()
        
    #     user=CustomUser.objects.create_user(username=validated_data['username'],
    #     email=validated_data['email'],password=validated_data['password'])
    #     user.save()
    #     return user
   
           
            
            
