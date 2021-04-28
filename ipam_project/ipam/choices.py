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
    STATUS_AVAILABLE = 'available'
