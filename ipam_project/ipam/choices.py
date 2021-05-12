from django.db import models


#
# IPAddress
#

class IPAddressStatusChoices(models.TextChoices):
    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'
    STATUS_DHCP = 'dhcp'


#
# IPPrefix
#

class IPPrefixStatusChoices(models.TextChoices):
    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'


#
# VLAN
#

class VLANStatusChoices(models.TextChoices):
    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'


#
# ServiceProtocol
#

class ServiceProtocolChoices(models.TextChoices):
    PROTOCOL_TCP = 'tcp'
    PROTOCOL_UDP = 'udp'


#
# DeviceComponents
#

class DeviceComponentStatusChoices(models.TextChoices):
    VIRTUAL = ' virtual'
    ETHERNET = 'ethernet'
    WIRELESS = 'wireless'
    SERIAL = 'serial'
