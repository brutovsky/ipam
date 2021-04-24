from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import password_validation

import sys
from django.core import exceptions
import django.contrib.auth.password_validation as validators

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def validate(self, data):
         # here data has all the fields which have validated values
         # so we can create a User instance out of it
         user = User(**data)

         # get the password from the data
         password = data.get('password')

         errors = dict()
         try:
             # validate the password and catch the exception
             validators.validate_password(password=password, user=User)

         # the exception raised here is different than serializers.ValidationError
         except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)

         if errors:
             raise serializers.ValidationError(errors)

         return super(CreateUserSerializer, self).validate(data)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# User serializer for admin view
class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users-api:user-detail')
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'groups', 'user_permissions', 'email', 'is_staff', 'is_superuser', 'last_login', 'date_joined']
        read_only_fields = ['username', 'last_login', 'date_joined']


# User serializer for admin view
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'id','groups', 'user_permissions',  'is_staff', 'is_superuser', 'last_login', 'date_joined']
        read_only_fields = ['id', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined']


# Custom token access and refresh pair serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
