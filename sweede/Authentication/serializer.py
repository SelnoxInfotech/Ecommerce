from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import datetime


Gender=(('M','MALE'),('F','FEMALE'))
#Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "first_name", "last_name", "username"]
    
#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  ConfirmPassword = serializers.CharField(write_only=True, required=True)
  Gender=serializers.ChoiceField(choices = Gender)
  DateOfBirth=serializers.DateField(default=datetime.date.today)
  class Meta:
    model = User
    fields = ('username', 'password', 'ConfirmPassword',
         'email', 'first_name', 'last_name','Gender','DateOfBirth')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['ConfirmPassword']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name'],
      Gender=validated_data['Gender'],
      DateOfBirth=validated_data['DateOfBirth']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user
    
