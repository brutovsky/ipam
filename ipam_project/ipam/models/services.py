from django.db import models
from ipam.models.ip import IPAddress
from ipam.choices import ServiceProtocolChoices
from django.core.validators import MaxValueValidator, MinValueValidator
from ipam.constants import SERVICE_PORT_MIN, SERVICE_PORT_MAX
from django.contrib.postgres.fields import ArrayField


__all__ = (
    'Service',
)


class Service(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
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
        verbose_name='Port numbers'
    )
    ip_addresses = models.ManyToManyField(
        IPAddress,
        related_name='services',
        blank=True,
        verbose_name='IP addresses'
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
