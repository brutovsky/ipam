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
from ipam import views as ipam_views


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_root(request):
    full_url = ''.join(['http://', get_current_site(request).domain, request.get_full_path()])
    content = {
        "DCIM api": f"{full_url}dcim/",
        "IPAM api": f"{full_url}ipam/",
        "Users api": f"{full_url}users/",
        "Groups api": f"{full_url}groups/",
        "Profile api": {
            "User profile": f"{full_url}account/profile",
            "Change password": f"{full_url}account/change-password",
        },
        "Token api": {
            "Obtain token": f"{full_url}token",
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

    'users': ('users/', 'users', 'Users Component'),
    'users-logs': ('users/users-logs/', 'users-logs', 'Logs'),
    'user-list': ('users/user-list/', 'user-list', 'Users'),
    'group-list': ('users/group-list/', 'group-list', 'Groups'),

    'ipam': ('ipam/', 'ipam', 'IPAM Component'),
    'ipam-logs': ('ipam/ipam-logs/', 'ipam-logs', 'Logs'),

    'prefix-list': ('ipam/prefix-list/', 'prefix-list', 'Prefixes'),
    'prefix-detail': ('ipam/prefix-list/prefix-detail/<int:pk>', 'prefix-detail', 'Prefix Detail'),
    'prefix-children': ('ipam/prefix-list/prefix-children/<int:pk>', 'prefix-children', 'Prefix Children'),
    'prefix-ip-addresses': ('ipam/prefix-list/prefix-ip-addresses/<int:pk>', 'prefix-ip-addresses', 'Prefix IP Addresses'),
    'prefix-logs': ('ipam/prefix-list/prefix-logs/<int:pk>', 'prefix-logs', 'Prefix Logs'),

    'ipaddress-list': ('ipam/ipaddress-list/', 'ipaddress-list', 'IP Addresses'),
    'ipaddress-detail': ('ipam/ipaddress-list/ipaddress-detail/<int:pk>', 'ipaddress-detail', 'IP Address Detail'),
    'ipaddress-logs': ('ipam/ipaddress-list/ipaddress-logs/<int:pk>', 'ipaddress-logs', 'IP Address Logs'),

    'service-list': ('ipam/service-list/', 'service-list', 'Services'),
    'service-detail': ('ipam/service-list/service-detail/<int:pk>', 'service-detail', 'Service Detail'),
    'service-logs': ('ipam/service-list/service-logs/<int:pk>', 'service-logs', 'Service Logs'),

    'interface-list': ('ipam/interface-list/', 'interface-list', 'Interfaces'),
    'interface-detail': ('ipam/interface-list/interface-detail/<int:pk>', 'interface-detail', 'Interface Detail'),
    'interface-logs': ('ipam/interface-list/interface-logs/<int:pk>', 'interface-logs', 'Interface Logs'),

    'iprole-list': ('ipam/iprole-list/', 'iprole-list', 'IP Roles'),

    'vlan-list': ('ipam/vlan-list/', 'vlan-list', 'VLAN'),
    'vlan-detail': ('ipam/vlan-list/vlan-detail/<int:pk>', 'vlan-detail', 'VLAN Detail'),
    'vlan-logs': ('ipam/vlan-list/vlan-logs/<int:pk>', 'vlan-logs', 'VLAN Logs'),
}

sidebar_navigation = {
    'Users Component': {
        'Logs': (
            pages['users-logs'],
            {
            }
        ),
        'Users': (
            pages['user-list'],
            {
            }
        ),
        'Groups': (
            pages['group-list'],
            {
            }
        )
    },

    'IPAM Component': {
        'Logs': (
            pages['ipam-logs'],
            {
            }
        ),
        'IP Roles': (
            pages['iprole-list'],
            {

            }
        ),
        'Prefixes': (
            pages['prefix-list'],
            {

            }
        ),
        'IP Addresses': (
            pages['ipaddress-list'],
            {

            }
        ),
        'Services': (
            pages['service-list'],
            {

            }
        ),
        'Interfaces': (
            pages['interface-list'],
            {

            }
        ),
        'VLAN': (
            pages['vlan-list'],
            {

            }
        )
    }
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

    path(pages['users'][0], user_views.user_component, name=pages['users'][1]),
    path(pages['users-logs'][0], user_views.users_logs, name=pages['users-logs'][1]),
    path(pages['user-list'][0], user_views.UserListView.as_view(), name=pages['user-list'][1]),
    path(pages['group-list'][0], user_views.GroupListView.as_view(), name=pages['group-list'][1]),

    path(pages['ipam'][0], ipam_views.ipam_component, name=pages['ipam'][1]),
    path(pages['ipam-logs'][0], ipam_views.ipam_logs, name=pages['ipam-logs'][1]),

    path(pages['iprole-list'][0], ipam_views.IPRoleListView.as_view(), name=pages['iprole-list'][1]),

    path(pages['prefix-list'][0], ipam_views.PrefixListView.as_view(), name=pages['prefix-list'][1]),
    path(pages['prefix-detail'][0], ipam_views.PrefixDetailView.as_view(), name=pages['prefix-detail'][1]),
    path(pages['prefix-children'][0], ipam_views.PrefixChildrenView.as_view(), name=pages['prefix-children'][1]),
    path(pages['prefix-ip-addresses'][0], ipam_views.PrefixIpAddressesView.as_view(), name=pages['prefix-ip-addresses'][1]),
    path(pages['prefix-logs'][0], ipam_views.PrefixLogsView.as_view(), name=pages['prefix-logs'][1]),

    path(pages['ipaddress-list'][0], ipam_views.IPAddressListView.as_view(), name=pages['ipaddress-list'][1]),
    path(pages['ipaddress-detail'][0], ipam_views.IPAddressDetailView.as_view(), name=pages['ipaddress-detail'][1]),
    path(pages['ipaddress-logs'][0], ipam_views.IPAddressLogsView.as_view(), name=pages['ipaddress-logs'][1]),

    path(pages['service-list'][0], ipam_views.ServiceListView.as_view(), name=pages['service-list'][1]),
    path(pages['service-detail'][0], ipam_views.ServiceDetailView.as_view(), name=pages['service-detail'][1]),
    path(pages['service-logs'][0], ipam_views.ServiceLogsView.as_view(), name=pages['service-logs'][1]),

    path(pages['interface-list'][0], ipam_views.InterfaceListView.as_view(), name=pages['interface-list'][1]),
    path(pages['interface-detail'][0], ipam_views.InterfaceDetailView.as_view(), name=pages['interface-detail'][1]),
    path(pages['interface-logs'][0], ipam_views.InterfaceLogsView.as_view(), name=pages['interface-logs'][1]),

    path(pages['vlan-list'][0], ipam_views.VLANListView.as_view(), name=pages['vlan-list'][1]),
    path(pages['vlan-detail'][0], ipam_views.VLANDetailView.as_view(), name=pages['vlan-detail'][1]),
    # path(pages['vlan-logs'][0], ipam_views.InterfaceLogsView.as_view(), name=pages['vlan-logs'][1]),
# 'post/<int:pk>/', PostDetailView.as_view(), name='post-detail'
]
