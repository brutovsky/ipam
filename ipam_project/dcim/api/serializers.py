from rest_framework import routers, serializers, viewsets
from dcim.models.site import Region, Site

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['name', 'description', 'parent']

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['name', 'status', 'region', 'description', 'physical_address', 'latitude', 'longitude', 'contact_name', 'contact_phone', 'contact_email']
