from rest_framework import routers, serializers, viewsets
from ipam.models.ip import *
from ipam.models.vlan import *
from ipam.models.service import *


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
    vlan = serializers.SlugRelatedField(
        queryset=VLAN.objects.all(),
        slug_field='name',
        allow_null=True
    )

    class Meta:
        model = IPPrefix
        fields = ['id', 'url', 'prefix', 'vlan', 'status', 'role', 'is_pool', 'description']

