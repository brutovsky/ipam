from django.db import models
from dcim.models.devices import Device
from ipam.models.ip import IPAddress
from ipam.models.vlan import VLAN
from dcim.choices import DeviceComponentStatusChoices


__all__ = (
    'Interface',
)


#
# Interfaces
#

class Interface(models.Model):
    enabled = models.BooleanField(
        default=True
    )
    device = models.ForeignKey(
        Device,
        related_name='interfaces',
        on_delete=models.PROTECT
    )
    name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    type = models.CharField(
        max_length=50,
        choices=DeviceComponentStatusChoices.choices,
        default=DeviceComponentStatusChoices.ETHERNET
    )
    untagged_vlan = models.ForeignKey(
        VLAN,
        on_delete=models.SET_NULL,
        related_name='interfaces_untagged',
        null=True,
        blank=True,
        verbose_name='Untagged VLAN'
    )
    tagged_vlans = models.ManyToManyField(
        VLAN,
        related_name='interfaces_tagged',
        blank=True,
        verbose_name='Tagged VLANs'
    )
    ip_addresses = models.ManyToManyField(
        IPAddress,
        related_name='interfaces',
        blank=True,
        verbose_name='IP addresses'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'ipam'