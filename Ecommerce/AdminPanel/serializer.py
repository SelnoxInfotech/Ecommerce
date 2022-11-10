from dataclasses import fields
from rest_framework import serializers
from .models import *
####################################################################################3
#Signup or log in#
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.models import User
# from rest_framework.validators import UniqueValidator
# from django.contrib.auth.password_validation import validate_password


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):           #login

#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         return token



# class UserRegisterSerializer(serializers.ModelSerializer):                  #signup
#     class Meta:
#         model = RegisterUser
#         fields = '__all__'
#     def register(self):
#         self.save()
#     def get_user_by_email(email):
#         try:
#             return RegisterUser.objects.get(email=email)
#         except:
#             return False
#     def isExists(self):
#         if RegisterUser.objects.filter(email=self.email):
#             return True
#         return False
########################################################################################################################################
class Serializer_Category(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class Serializer_SubCategory(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        

class Serializer_Country(serializers.ModelSerializer):
    class Meta:
        model=Countries
        fields='__all__'
        
class Serializer_States(serializers.ModelSerializer):
    class Meta:
        model=States
        fields='__all__'
        
class Serializer_Cities(serializers.ModelSerializer):
    class Meta:
        model=Cities
        fields='__all__'
        
class Serializer_StrainType(serializers.ModelSerializer):
    class Meta:
        model=StrainType
        fields='__all__'
        
class Serializer_LabResult(serializers.ModelSerializer):
    class Meta:
        model=LabResults
        fields='__all__'
        
class Serializer_Product(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='Product_Name','Category','Strain_Types','prices','lab_Result','net_weight','Product_Image','Country','City','State'
        
class Serializer_Brand(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'
        
        
        
        
        
        
        
        
        
        
        
        
        