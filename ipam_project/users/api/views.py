from django.contrib.auth.models import User
from .serializers import CreateUserSerializer, UserSerializer, MyTokenObtainPairSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.decorators import permission_required

from django.contrib.auth.mixins import PermissionRequiredMixin

from users.permissions import IsAdmin

from rest_framework import generics
from rest_framework import viewsets

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


#
# User list view for admin
#
class UserList(APIView):
    """
    `List` all users.
    """
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)


#
# User detail view for admin
#
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    `Retrieve`, `update` and `delete` users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)


# Custome token access and refresh pair view
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
