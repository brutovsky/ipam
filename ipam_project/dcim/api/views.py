from .serializers import *
from dcim.models.site import *
from dcim.models.rack import *
from rest_framework import viewsets


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


#
# RackGroup View
#
class RackGroupViewSet(viewsets.ModelViewSet):
    queryset = RackGroup.objects.all()
    serializer_class = RackGroupSerializer


#
# RackRole View
#
class RackRoleViewSet(viewsets.ModelViewSet):
    queryset = RackRole.objects.all()
    serializer_class = RackRoleSerializer


#
# Rack View
#
class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
