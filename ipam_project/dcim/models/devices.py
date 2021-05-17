from django.db import models
from ipam_project.widgets import ColorField
from dcim.choices import DeviceStatusChoices
from dcim.models.racks import Rack


__all__ = (
    'Manufacturer',
    'Platform',
    'DeviceType',
    'DeviceRole',
    'Device'
)


#
# Manufacturers
#

class Manufacturer(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'dcim'


#
# Platforms
#

class Platform(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        related_name='platforms',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'dcim'


#
# DeviceTypes
#

class DeviceType(models.Model):
    manufacturer = models.ForeignKey(
        Manufacturer,
        related_name='device_types',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    model = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.model

    class Meta:
        ordering = ['model']
        app_label = 'dcim'


#
# DeviceRoles
#

class DeviceRole(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    color = ColorField(
        default='#ffffff'
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'dcim'


#
# Devices
#

class Device(models.Model):
    type = models.ForeignKey(
        DeviceType,
        related_name='devices',
        on_delete=models.PROTECT,
    )
    role = models.ForeignKey(
        DeviceRole,
        related_name='devices',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Functional role'
    )
    platform = models.ForeignKey(
        Platform,
        related_name='devices',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=100,
        unique=True
    )
    serial = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Serial number'
    )
    rack = models.ForeignKey(
        Rack,
        related_name='devices',
        on_delete=models.PROTECT,
    )
    status = models.CharField(
        max_length=50,
        choices=DeviceStatusChoices.choices,
        default=DeviceStatusChoices.STATUS_ACTIVE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'dcim'