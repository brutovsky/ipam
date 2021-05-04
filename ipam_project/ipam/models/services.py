from django.core.exceptions import ValidationError
from django.db import models
from ipam.models.ip import IPAddress
from ipam.choices import ServiceProtocolChoices
from django.core.validators import MaxValueValidator, MinValueValidator
from ipam.constants import SERVICE_PORT_MIN, SERVICE_PORT_MAX
from django.contrib.postgres.fields import ArrayField
from dcim.models.devices import Device
from ipam.models.device_components import Interface


__all__ = (
    'Service',
)


class Service(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='device'
    )
    protocol = models.CharField(
        max_length=50,
        choices=ServiceProtocolChoices.choices
    )
    ports = ArrayField(
        base_field=models.PositiveIntegerField(
            validators=[
                MinValueValidator(SERVICE_PORT_MIN),
                MaxValueValidator(SERVICE_PORT_MAX)
            ]
        ),
        verbose_name='Port numbers',
        help_text='Enter numbers separated with commas(80,3000)'
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    def clean(self):
        super().clean()

        if self.ip_addresses:
            for ip_addr in self.ip_addresses.all():
                ip_addr.full_clean()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'ipam'
