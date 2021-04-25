from rest_framework import routers, serializers, viewsets
from dcim.models.site import Region, Site

class RegionSerializer(serializers.ModelSerializer):
    sites = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='dcim_api:site-detail',
        lookup_field='name'
    )
    parent = serializers.SlugRelatedField(
        queryset = Region.objects.all(),
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
