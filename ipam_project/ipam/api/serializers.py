from rest_framework import routers, serializers, viewsets
from ipam.models.ip import *
from ipam.models.vlan import *
from ipam.models.services import *
from dcim.models.locations import Location
from dcim.models.devices import Device
from ipam.models.device_components import *


#
# IP module
#

class IPRoleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='ipam_api:ip_role-detail',
    )
    ip_addresses = serializers.HyperlinkedIdentityField(
        many=True,
        read_only=True,
        view_name='ipam_api:ip_address-detail',
    )
    ip_prefixes = serializers.HyperlinkedIdentityField(
        many=True,
        read_only=True,
        view_name='ipam_api:ip_prefix-detail',
    )

    class Meta:
        model = IPRole
        fields = ['id', 'url', 'name', 'description', 'ip_addresses', 'ip_prefixes']


class IPAddressSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='ipam_api:ip_address-detail',
    )

    class Meta:
        model = IPAddress
        fields = ['id', 'url', 'address', 'status', 'role', 'dns_name', 'description']


class IPPrefixSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='ipam_api:ip_prefix-detail',
    )
    location = serializers.SlugRelatedField(
        queryset=Location.objects.all(),
        slug_field='name',
        allow_null=True
    )
    vlan = serializers.SlugRelatedField(
        queryset=VLAN.objects.all(),
        slug_field='name',
        allow_null=True
    )

    class Meta:
        model = IPPrefix
        fields = ['id', 'url', 'prefix', 'location', 'vlan', 'status', 'role', 'is_pool', 'description', 'ip_addresses']


#
# VLAN module
#

class VLANRoleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='ipam_api:vlan_role-detail',
    )
    vlans = serializers.HyperlinkedIdentityField(
        many=True,
        read_only=True,
        view_name='ipam_api:vlan-detail',
    )

    class Meta:
        model = VLANRole
        fields = ['id', 'url', 'name', 'description', 'vlans']


class VLANGroupSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='ipam_api:vlan_group-detail',
    )
    location = serializers.SlugRelatedField(
        queryset=Location.objects.all(),
        slug_field='name',
        allow_null=True
    )
    vlans = serializers.HyperlinkedIdentityField(
        many=True,
        read_only=True,
        view_name='ipam_api:vlan-detail',
    )

    class Meta:
        model = VLANGroup
        fields = ['id', 'url', 'name', 'description', 'location', 'vlans']


class VLANSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='ipam_api:vlan-detail',
    )

    class Meta:
        model = VLAN
        fields = ['id', 'url', 'vid', 'name', 'status', 'role', 'description']


#
# Service module
#

class ServiceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='ipam_api:service-detail',
    )

    class Meta:
        model = Service
        fields = ['id', 'url', 'name', 'protocol', 'ports', 'ip_addresses', 'description']


#
# DeviceComponent module
#

class InterfaceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='ipam_api:interface-detail',
    )
    device = serializers.SlugRelatedField(
        queryset=Device.objects.all(),
        slug_field='name'
    )
    untagged_vlan = serializers.SlugRelatedField(
        queryset=VLAN.objects.all(),
        slug_field='name',
        allow_null=True
    )
    tagged_vlan = serializers.SlugRelatedField(
        queryset=VLAN.objects.all(),
        slug_field='name',
        allow_null=True
    )

    class Meta:
        model = Interface
        fields = ['id', 'url', 'enabled', 'device', 'description', 'type', 'untagged_vlan', 'tagged_vlan', 'ip_addresses']
