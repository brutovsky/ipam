from django.db import models

from dcim.choices import *

__all__ = (
    'Region',
    'Location',
)

#
# Regions
#

class Region(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    parent = models.ForeignKey(
        to='self',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'dcim'


#
# Locations
#

class Location(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    status = models.CharField(
        max_length=50,
        choices=SiteStatusChoices.choices,
        default=SiteStatusChoices.STATUS_ACTIVE
    )
    region = models.ForeignKey(
        Region,
        related_name='locations',
        on_delete=models.PROTECT
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    physical_address = models.CharField(
        max_length=200,
        blank=True
    )
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        blank=True,
        null=True,
        help_text='GPS coordinate (latitude)'
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text='GPS coordinate (longitude)'
    )
    contact_name = models.CharField(
        max_length=50,
        blank=True
    )
    contact_phone = models.CharField(
        max_length=20,
        blank=True
    )
    contact_email = models.EmailField(
        blank=True,
        verbose_name='Contact E-mail'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'dcim'
