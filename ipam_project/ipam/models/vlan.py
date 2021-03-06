from django.core.exceptions import ValidationError
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
        on_delete=models.PROTECT
    )

    def clean(self):
        super().clean()

        if not hasattr(self, 'location'):
            raise ValidationError('Location is required')

        if self.vlans:
            for vlan in self.vlans.all():
                vlan.full_clean()

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
        unique=False
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

    def clean(self):
        super().clean()

        if self.ip_prefixes:
            for ip_prefix in self.ip_prefixes.all():
                ip_prefix.full_clean()

    def __str__(self):
        return f'{self.vlan_group}:{self.name}'

    class Meta:
        ordering = ['vid']
        app_label = 'ipam'
        unique_together = [['name', 'vlan_group']]
