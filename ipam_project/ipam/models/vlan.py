from django.db import models
from dcim.models.locations import Location
from django.core.validators import MaxValueValidator, MinValueValidator
from ipam.choices import VLANStatusChoices
from ipam.constants import VLAN_VID_MIN, VLAN_VID_MAX


__all__ = (
    'VLANRole',
    'VLANGroup',
    'VLAN',
)


#
# VLANRole
#

class VLANRole(models.Model):
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
        app_label = 'ipam'


#
# VLANGroup
#

class VLANGroup(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    location = models.ForeignKey(
        Location,
        related_name='vlan_groups',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'ipam'


#
# VLAN
#

class VLAN(models.Model):
    vlan_group = models.ForeignKey(
        VLANGroup,
        related_name='vlans',
        on_delete=models.PROTECT,
    )
    vid = models.PositiveSmallIntegerField(
        verbose_name='VLAN ID',
        validators=[MinValueValidator(VLAN_VID_MIN), MaxValueValidator(VLAN_VID_MAX)],
        help_text='VLAN IDs need to be unique within a VLANGroup'
    )
    name = models.CharField(
        max_length=100,
        unique=True
    )
    status = models.CharField(
        max_length=50,
        choices=VLANStatusChoices.choices,
        default=VLANStatusChoices.STATUS_ACTIVE
    )
    role = models.ForeignKey(
        VLANRole,
        related_name='vlans',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Functional role'
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['vid']
        app_label = 'ipam'
