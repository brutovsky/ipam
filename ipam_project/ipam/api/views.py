from .serializers import *
from ipam.models.ip import *
from ipam.models.vlan import *
from ipam.models.service import *
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
