from django.db import models
from .site import Site
from dcim.choices import *
from ipam_project.widgets import *


__all__ = (
    'RackGroup',
    'RackRole',
    'Rack',
)


#
# RackGroups
#

class RackGroup(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    site = models.ForeignKey(
        Site,
        related_name='rack_groups',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    parent = models.ForeignKey(
        to='self',
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
# RackRoles
#

class RackRole(models.Model):
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
# Racks
#

class Rack(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    rack_group = models.ForeignKey(
        RackGroup,
        related_name='racks',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=50,
        choices=RackStatusChoices.choices,
        default=RackStatusChoices.STATUS_AVAILABLE
    )

    role = models.ForeignKey(
        RackRole,
        related_name='racks',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Functional role'
    )

    serial = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Serial number'
    )

    type = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'dcim'
