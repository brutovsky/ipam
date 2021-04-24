from django.contrib.auth.models import User, Group
from .serializers import CreateUserSerializer, UserProfileSerializer, UserSerializer, GroupSerializer, MyTokenObtainPairSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView

from users.permissions import IsAdmin

from rest_framework import generics
from rest_framework import viewsets

#
# User create view
#
class UserCreate(generics.CreateAPIView):
    """
    `Create` a new user.
    """
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


#
# Group list view for admin
#
class GroupList(APIView):
    """
    `List` all groups.
    """
    permission_classes = (IsAdmin,)

    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True, context={'request': request})
        return Response(serializer.data)


#
# Group detail view for admin
#
class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    `Retrieve`, `update` and `delete` groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdmin,)


class UserProfileDetail(APIView):
    """
    `Retrieve` and `update` user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(request.user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# Custome token access and refresh pair view
#
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
