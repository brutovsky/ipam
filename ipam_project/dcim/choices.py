from django.db import models


#
# Sites
#

class SiteStatusChoices(models.TextChoices):
    STATUS_PLANNED = 'planned'
    STATUS_STAGING = 'staging'
    STATUS_ACTIVE = 'active'
    STATUS_DECOMMISSIONING = 'decommissioning'
    STATUS_RETIRED = 'retired'


#
# Racks
#

class RackStatusChoices(models.TextChoices):
    STATUS_RESERVED = 'reserved'
    STATUS_AVAILABLE = 'available'
    STATUS_ACTIVE = 'active'


#
# Devices
#

class DeviceStatusChoices(models.TextChoices):
    STATUS_OFFLINE = 'offline'
    STATUS_ACTIVE = 'active'

