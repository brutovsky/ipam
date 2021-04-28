from rest_framework import routers, serializers, viewsets
from dcim.models.site import *
from dcim.models.rack import *
from dcim.models.device import *


#
# Site module
#

class RegionSerializer(serializers.ModelSerializer):
    sites = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dcim_api:site-detail',
        lookup_field='name'
    )
    parent = serializers.SlugRelatedField(
        queryset=Region.objects.all(),
        slug_field='name',
        allow_null=True
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:region-detail',
        lookup_field='name'
    )

    class Meta:
        model = Region
        fields = ['id', 'url', 'name', 'description', 'parent', 'sites']


class SiteSerializer(serializers.ModelSerializer):
    region = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='dcim_api:region-detail',
        lookup_field='name'
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:site-detail',
        lookup_field='name'
    )

    class Meta:
        model = Site
        fields = ['id', 'url', 'name', 'status', 'description', 'physical_address', 'latitude', 'longitude', 'contact_name', 'contact_phone', 'contact_email', 'region']


#
# Rack module
#

class RackGroupSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:rack_group-detail',
    )
    parent = serializers.SlugRelatedField(
        queryset=RackGroup.objects.all(),
        slug_field='name',
        allow_null=True
    )
    site = serializers.SlugRelatedField(
        queryset=Site.objects.all(),
        slug_field='name',
        allow_null=True
    )
    racks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dcim_api:rack-detail'
    )

    class Meta:
        model = RackGroup
        fields = ['id', 'url', 'name', 'site', 'parent', 'description', 'racks']


class RackRoleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:rack_role-detail',
    )
    racks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dcim_api:rack-detail'
    )

    class Meta:
        model = RackRole
        fields = ['id', 'url', 'name', 'color', 'description', 'racks']


class RackSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:rack-detail',
    )
    rack_group = serializers.SlugRelatedField(
        queryset=RackGroup.objects.all(),
        slug_field='name',
        allow_null=True
    )
    rack_role = serializers.SlugRelatedField(
        queryset=RackRole.objects.all(),
        slug_field='name',
        allow_null=True
    )

    class Meta:
        model = Rack
        fields = ['id', 'url', 'name', 'rack_group', 'status', 'rack_role', 'serial', 'type']


#
# Device module
#

class ManufacturerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:platform-detail',
    )
    platforms = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dcim_api:platform-detail'
    )
    device_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dcim_api:device_type-detail'
    )

    class Meta:
        model = Manufacturer
        fields = ['id', 'url', 'name', 'description', 'platforms', 'device_types']


class PlatformSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:platform-detail',
    )
    manufacturer = serializers.SlugRelatedField(
        queryset=Manufacturer.objects.all(),
        slug_field='name',
        allow_null=True
    )
    devices = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dcim_api:device-detail'
    )

    class Meta:
        model = Platform
        fields = ['id', 'url', 'name', 'manufacturer', 'description', 'devices']


class DeviceTypeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:device_type-detail',
    )
    manufacturer = serializers.SlugRelatedField(
        queryset=Manufacturer.objects.all(),
        slug_field='name',
        allow_null=True
    )
    devices = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dcim_api:device-detail'
    )

    class Meta:
        model = DeviceType
        fields = ['id', 'url', 'manufacturer', 'model', 'devices']


class DeviceRoleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:device_role-detail',
    )
    devices = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dcim_api:device-detail'
    )

    class Meta:
        model = DeviceRole
        fields = ['id', 'url', 'name', 'color', 'description', 'devices']


class DeviceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='dcim_api:device_role-detail',
    )
    type = serializers.SlugRelatedField(
        queryset=DeviceType.objects.all(),
        slug_field='model',
        allow_null=True
    )
    role = serializers.SlugRelatedField(
        queryset=DeviceRole.objects.all(),
        slug_field='name',
        allow_null=True
    )
    platform = serializers.SlugRelatedField(
        queryset=Platform.objects.all(),
        slug_field='name',
        allow_null=True
    )
    rack = serializers.SlugRelatedField(
        queryset=Rack.objects.all(),
        slug_field='name',
        allow_null=True
    )

    class Meta:
        model = Device
        fields = ['id', 'url', 'type', 'role', 'platform', 'name', 'serial', 'rack', 'status', 'mac_address']