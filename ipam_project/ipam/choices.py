from django.db import models


#
# IPAddress
#

class IPAddressChoices(models.TextChoices):
    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'
    STATUS_DHCP = 'dhcp'


#
# IPPrefix
#

class IPPrefixChoices(models.TextChoices):
    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'
