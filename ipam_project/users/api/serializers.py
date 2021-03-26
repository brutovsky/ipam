from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'groups', 'user_permissions', 'email', 'is_staff', 'is_superuser', 'last_login', 'date_joined']
        #extra_kwargs = {'username': {'required': False}}
