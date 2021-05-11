from .serializers import *
from ipam.models.ip import *
from ipam.models.vlan import *
from ipam.models.services import *
from rest_framework import viewsets


#
# IPRole View
#
class IPRoleViewSet(viewsets.ModelViewSet):
    queryset = IPRole.objects.all()
    serializer_class = IPRoleSerializer


#
# IPAddress View
#
class IPAddressViewSet(viewsets.ModelViewSet):
    queryset = IPAddress.objects.all()
    serializer_class = IPAddressSerializer


#
# IPPrefix View
#
class IPPrefixViewSet(viewsets.ModelViewSet):
    queryset = IPPrefix.objects.all()
    serializer_class = IPPrefixSerializer


#
# VLANRole View
#
class VLANRoleViewSet(viewsets.ModelViewSet):
    queryset = VLANRole.objects.all()
    serializer_class = VLANRoleSerializer


#
# VLANGroup View
#
class VLANGroupViewSet(viewsets.ModelViewSet):
    queryset = VLANGroup.objects.all()
    serializer_class = VLANGroupSerializer


#
# VLAN View
#
class VLANViewSet(viewsets.ModelViewSet):
    queryset = VLAN.objects.all()
    serializer_class = VLANSerializer


#
# Service View
#
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


#
# Interface View
#
class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
