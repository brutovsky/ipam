"""ipam_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, schema, permission_classes
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site

# Front
from django.contrib.auth import views as auth_views
from users import views as user_views

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def api_root(request):
    full_url = ''.join(['http://', get_current_site(request).domain, request.get_full_path()])
    content = {
        "DCIM api": f"{full_url}dcim/",
        "IPAM api": f"{full_url}ipam/",
        "Users api": f"{full_url}users/",
        "Groups api": f"{full_url}groups/",
        "Profile api": {
            "User profile" : f"{full_url}account/profile",
            "Change password": f"{full_url}account/change-password",
        },
        "Token api": {
            "Obtain token" : f"{full_url}token",
            "Refresh token": f"{full_url}token/refresh",
        },
        "Auth api": {
            "Login": f"{full_url}auth/login",
            "Logout": f"{full_url}auth/logout",
        },
    }
    return Response(content)


pages = {
    '': ('', 'home', 'Home'),
    'profile': ('profile/', 'profile', 'Profile'),
    'login': ('login/', 'login', 'Login'),
    'register': ('register/', 'register', 'Registration'),
    'change-password': ('change-password/', 'change-password', 'Change Password'),
    'logout': ('logout/', 'logout', 'Logout'),

    'users': ('users/', 'users', 'Users component'),
    'user-list': ('users/user-list/', 'user-list', 'Users'),
    'group-list': ('users/group-list/', 'group-list', 'Groups'),
}

sidebar_navigation = {
    'Users Component': (
        ('users/', 'users', 'Users'),
        {
            'user-list': pages['user-list'],
            'group-list': pages['group-list']
        }
    )
# ,
#     'IPAM': [
#         ('users/', 'users', 'Users'),
#         {
#         }
#     ]
}


urlpatterns = [
    # Admin page
    path('admin/', admin.site.urls),
    # Api
    path('api/', api_root),
    path('api/', include('users.api.urls')),
    path('api/dcim/', include('dcim.api.urls', namespace='api_dcim')),
    path('api/ipam/', include('ipam.api.urls', namespace='api_ipam')),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Pages
    path(pages['login'][0], auth_views.LoginView.as_view(template_name='users/login.html'), name=pages['login'][1]),
    path(pages['logout'][0], auth_views.LogoutView.as_view(template_name='users/logout.html'), name=pages['logout'][1]),
    path(pages['register'][0], user_views.register, name=pages['register'][1]),
    path(pages['profile'][0], user_views.profile, name=pages['profile'][1]),
    path(pages['change-password'][0], user_views.change_password, name=pages['change-password'][1]),
    path(pages[''][0], user_views.profile, name=pages[''][1]),

    path(pages['users'][0], user_views.UserComponentView.as_view(), name=pages['users'][1]),
    path(pages['user-list'][0], user_views.UserListView.as_view(), name=pages['user-list'][1]),
    path(pages['group-list'][0], user_views.UserListView.as_view(), name=pages['group-list'][1]),
]
