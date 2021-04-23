from .serializers import RegionSerializer, SiteSerializer
from dcim.models.site import Region, Site

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from rest_framework import permissions

#
# Region View
#
class RegionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = 'name'
    permission_classes = [permissions.IsAuthenticated]


#
# Site View
#
class SiteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    lookup_field = 'name'
    permission_classes = [permissions.IsAuthenticated]
