from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.shortcuts import render
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
from dcim import views as dcim_views

from dcim.models.devices import Device
from ipam.models.ip import IPPrefix


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

    # IPAM
    'ipam': ('ipam/', 'ipam', 'IPAM Component'),
    'ipam-logs': ('ipam/ipam-logs/', 'ipam-logs', 'Logs'),

    'prefix-list': ('ipam/prefix-list/', 'prefix-list', 'Prefixes'),
    'prefix-detail': ('ipam/prefix-list/prefix-detail/<int:pk>', 'prefix-detail', 'Prefix Detail'),
    'prefix-children': ('ipam/prefix-list/prefix-children/<int:pk>', 'prefix-children', 'Prefix Children'),
    'prefix-ip-addresses': (
        'ipam/prefix-list/prefix-ip-addresses/<int:pk>', 'prefix-ip-addresses', 'Prefix IP Addresses'),
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
    'vlan-prefixes': ('ipam/vlan-list/vlan-prefixes/<int:pk>', 'vlan-prefixes', 'VLAN Prefixes'),

    'vlangroup-list': ('ipam/vlangroup-list/', 'vlangroup-list', 'VLAN Groups'),

    'vlanrole-list': ('ipam/vlanrole-list/', 'vlanrole-list', 'VLAN Roles'),

    # DCIM
    'dcim': ('dcim/', 'dcim', 'DCIM Component'),
    'dcim-logs': ('dcim/dcim-logs/', 'dcim-logs', 'Logs'),

    'region-list': ('dcim/region-list/', 'region-list', 'Regions'),

    'location-list': ('dcim/location-list/', 'location-list', 'Locations'),
    'location-detail': ('dcim/location-list/location-detail/<int:pk>', 'location-detail', 'Location Detail'),
    'location-rackgroups': (
        'dcim/location-list/location-rackgroups/<int:pk>', 'location-rackgroups', 'Location Rack groups'),
    'location-prefixes': (
        'dcim/location-list/location-prefixes/<int:pk>', 'location-prefixes', 'Location Prefixes'),
    'location-vlangroups': (
        'dcim/location-list/location-vlangroups/<int:pk>', 'location-vlangroups', 'Location VLAN Groups'),
    'location-statistics': (
        'dcim/location-list/location-statistics/<int:pk>', 'location-statistics', 'Location Statistics'),
    'location-logs': (
        'dcim/location-list/location-logs/<int:pk>', 'location-logs', 'Location Logs'),

    'rackgroup-list': ('dcim/rackgroup-list/', 'rackgroup-list', 'Rack Groups'),

    'rackrole-list': ('dcim/rackrole-list/', 'rackrole-list', 'Rack Roles'),

    'rack-list': ('dcim/rack-list/', 'rack-list', 'Racks'),
    'rack-detail': ('dcim/rack-list/rack-detail/<int:pk>', 'rack-detail', 'Rack Detail'),
    'rack-devices': ('dcim/rack-list/rack-devices/<int:pk>', 'rack-devices', 'Rack Devices'),
    'rack-logs': ('dcim/rack-list/rack-logs/<int:pk>', 'rack-logs', 'Rack Logs'),

    'manufacturer-list': ('dcim/manufacturer-list/', 'manufacturer-list', 'Manufacturers'),

    'platform-list': ('dcim/platform-list/', 'platform-list', 'Platforms'),

    'devicetype-list': ('dcim/devicetype-list/', 'devicetype-list', 'Device Types'),

    'devicerole-list': ('dcim/devicerole-list/', 'devicerole-list', 'Device Roles'),

    'device-list': ('dcim/device-list/', 'device-list', 'Devices'),
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
        'VLAN Roles': (
            pages['vlanrole-list'],
            {

            }
        ),
        'VLAN Groups': (
            pages['vlangroup-list'],
            {

            }
        ),
        'VLANs': (
            pages['vlan-list'],
            {

            }
        )
    },

    'DCIM Component': {
        'Logs': (
            pages['dcim-logs'],
            {
            }
        ),
        'Regions': (
            pages['region-list'],
            {
            }
        ),
        'Locations': (
            pages['location-list'],
            {
            }
        ),
        'Rack Group': (
            pages['rackgroup-list'],
            {
            }
        ),
        'Rack Roles': (
            pages['rackrole-list'],
            {
            }
        ),
        'Racks': (
            pages['rack-list'],
            {
            }
        ),
        'Manufacturers': (
            pages['manufacturer-list'],
            {
            }
        ),
        'Platforms': (
            pages['platform-list'],
            {
            }
        ),
        'Device Types': (
            pages['devicetype-list'],
            {
            }
        ),
        'Device Roles': (
            pages['devicerole-list'],
            {
            }
        ),
        'Devices': (
            pages['device-list'],
            {
            }
        ),
    }
}


def home(request):
    logs = LogEntry.objects.order_by('-action_time')[:10]

    statistics = {
        'IPAM': {},
        'DCIM': {},
        'Users': {},
    }

    statistics['IPAM']['Number of prefixes'] = IPPrefix.objects.all().count()
    statistics['DCIM']['Number of device'] = Device.objects.all().count()
    statistics['Users']['Number of users'] = User.objects.all().count()

    return render(request, 'home.html', {
        'logs': logs,
        'statistics': statistics
    })


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
    path(pages[''][0], home, name=pages[''][1]),

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
    path(pages['prefix-ip-addresses'][0], ipam_views.PrefixIpAddressesView.as_view(),
         name=pages['prefix-ip-addresses'][1]),
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
    path(pages['vlan-logs'][0], ipam_views.VLANLogsView.as_view(), name=pages['vlan-logs'][1]),
    path(pages['vlan-prefixes'][0], ipam_views.VLANPrefixesView.as_view(), name=pages['vlan-prefixes'][1]),

    path(pages['vlangroup-list'][0], ipam_views.VLANGroupListView.as_view(), name=pages['vlangroup-list'][1]),

    path(pages['vlanrole-list'][0], ipam_views.VLANRoleListView.as_view(), name=pages['vlanrole-list'][1]),

    # DCIM
    path(pages['dcim'][0], dcim_views.dcim_component, name=pages['dcim'][1]),
    path(pages['dcim-logs'][0], dcim_views.dcim_logs, name=pages['dcim-logs'][1]),

    path(pages['region-list'][0], dcim_views.RegionListView.as_view(), name=pages['region-list'][1]),

    path(pages['location-list'][0], dcim_views.LocationListView.as_view(), name=pages['location-list'][1]),
    path(pages['location-detail'][0], dcim_views.LocationDetailView.as_view(), name=pages['location-detail'][1]),
    path(pages['location-rackgroups'][0], dcim_views.LocationRackGroupsView.as_view(),
         name=pages['location-rackgroups'][1]),
    path(pages['location-prefixes'][0], dcim_views.LocationPrefixesView.as_view(),
         name=pages['location-prefixes'][1]),
    path(pages['location-vlangroups'][0], dcim_views.LocationVLANGroupsView.as_view(),
         name=pages['location-vlangroups'][1]),
    path(pages['location-statistics'][0], dcim_views.LocationStatisticsView.as_view(),
         name=pages['location-statistics'][1]),
    path(pages['location-logs'][0], dcim_views.LocationLogsView.as_view(),
         name=pages['location-logs'][1]),

    path(pages['rackgroup-list'][0], dcim_views.RackGroupListView.as_view(), name=pages['rackgroup-list'][1]),

    path(pages['rackrole-list'][0], dcim_views.RackRoleListView.as_view(), name=pages['rackrole-list'][1]),

    path(pages['rack-list'][0], dcim_views.RackListView.as_view(), name=pages['rack-list'][1]),
    path(pages['rack-detail'][0], dcim_views.RackDetailView.as_view(), name=pages['rack-detail'][1]),
    path(pages['rack-devices'][0], dcim_views.RackDevicesView.as_view(), name=pages['rack-devices'][1]),
    path(pages['rack-logs'][0], dcim_views.RackLogsView.as_view(), name=pages['rack-logs'][1]),

    path(pages['manufacturer-list'][0], dcim_views.ManufacturerListView.as_view(), name=pages['manufacturer-list'][1]),

    path(pages['platform-list'][0], dcim_views.PlatformListView.as_view(), name=pages['platform-list'][1]),

    path(pages['devicetype-list'][0], dcim_views.DeviceTypeListView.as_view(), name=pages['devicetype-list'][1]),

    path(pages['devicerole-list'][0], dcim_views.DeviceRoleListView.as_view(), name=pages['devicerole-list'][1]),

    path(pages['device-list'][0], dcim_views.DeviceListView.as_view(), name=pages['device-list'][1]),

]
