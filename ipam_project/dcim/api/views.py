from .serializers import *
from dcim.models.locations import *
from dcim.models.racks import *
from dcim.models.devices import *
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
# Location View
#
class LocationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
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


#
# Manufacturer View
#
class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


#
# Platform View
#
class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


#
# DeviceType View
#
class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


#
# DeviceRole View
#
class DeviceRoleViewSet(viewsets.ModelViewSet):
    queryset = DeviceRole.objects.all()
    serializer_class = DeviceRoleSerializer


#
# Device View
#
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
