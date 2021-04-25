from rest_framework import routers, serializers, viewsets
from dcim.models.site import *
from dcim.models.rack import *


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