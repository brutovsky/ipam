from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from ipam.choices import IPAddressStatusChoices, IPPrefixStatusChoices
from ipam.fields import IPAddressField, IPNetworkField
from ipam import validators
from ipam.models.vlan import VLAN
from dcim.models.locations import Location
from netaddr import IPNetwork, IPSet
from dcim.utils import toset

__all__ = (
    'IPRole',
    'IPAddress',
    'IPPrefix',
)


#
# IPRole
#


class IPRole(models.Model):
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
# IPPrefixes
#

class IPPrefix(models.Model):
    prefix = IPNetworkField(
        help_text='IPv4 or IPv6 network with mask'
    )
    is_container = models.BooleanField(
        verbose_name='Is a container',
        default=False,
        help_text='Other IP prefixes can be nested inside this prefix '
    )
    prefix_container = models.ForeignKey(
        to='self',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={'is_container': True},
        help_text='Choose prefix container if this prefix is nested',
    )
    location = models.ForeignKey(
        Location,
        related_name='ip_prefixes',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    vlan = models.ForeignKey(
        VLAN,
        related_name='ip_prefixes',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=50,
        choices=IPPrefixStatusChoices.choices,
        default=IPPrefixStatusChoices.STATUS_ACTIVE
    )
    role = models.ForeignKey(
        IPRole,
        related_name='ip_prefixes',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Functional role'
    )
    is_pool = models.BooleanField(
        verbose_name='Is a pool',
        default=True,
        help_text='All IP addresses within this prefix are considered usable'
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    def clean(self):
        super().clean()

        if self.is_container:
            self.vlan = None
            self.is_pool = False

        subnet = IPSet([self.prefix])

        if self.prefix and self.prefix_container:
            container = IPSet([self.prefix_container.prefix])
            if not container > subnet:
                raise ValidationError(f'{subnet} is not subnet of {container}')
            container_children = map(toset, IPPrefix.objects.filter(prefix_container=self.prefix_container))
            for child in container_children:
                if len(child & subnet) != 0:
                    raise ValidationError(f'{subnet} overlaps with {child}')

        else:
            all_ip_sets = map(toset, IPPrefix.objects.all().exclude(pk=self.pk))
            for ip_set in all_ip_sets:
                if len(ip_set & subnet) != 0:
                    raise ValidationError(f'{subnet} overlaps with {ip_set}')

    def __str__(self):
        label = 'Container' if self.is_container else ('Pool' if self.is_pool else 'Default')
        return str(f'{label}:{self.prefix}')

    class Meta:
        ordering = ['prefix']
        app_label = 'ipam'


#
# IPAddress
#

class IPAddress(models.Model):
    address = IPAddressField(
        help_text='IPv4 or IPv6 address (with mask)'
    )
    prefix = models.ForeignKey(
        IPPrefix,
        related_name='ip_addresses',
        on_delete=models.PROTECT,
        limit_choices_to={'is_container': False},
        verbose_name='Network prefix'
    )
    status = models.CharField(
        max_length=50,
        choices=IPAddressStatusChoices.choices,
        default=IPAddressStatusChoices.STATUS_ACTIVE
    )
    role = models.ForeignKey(
        IPRole,
        related_name='ip_addresses',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Functional role'
    )
    dns_name = models.CharField(
        max_length=255,
        validators=[validators.DNSValidator],
        blank=True,
        null=True,
        verbose_name='DNS Name',
        help_text='Hostname'
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    assigned_interface = models.ForeignKey(
        to='ipam.interface',
        related_name='ip_addresses',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if hasattr(self, 'dns_name') and self.dns_name:
            self.dns_name = self.dns_name.lower()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.address and hasattr(self, 'prefix'):
            if self.address.prefixlen == 0:
                raise ValidationError({
                    'address': "Cannot create IP address with /0 mask."
                })
            if IPNetwork(self.address) != self.prefix.prefix:
                raise ValidationError('IP Address network and prefix does not match')

        all_ip_addresses = IPAddress.objects.all().exclude(pk=self.pk)
        for ip_address in all_ip_addresses:
            if self.dns_name and self.dns_name == ip_address.dns_name:
                raise ValidationError(f'{self.address} dns name already exist')

    def __str__(self):
        return str(f'{f"{self.dns_name}:" if self.dns_name else ""}{self.address}')

    class Meta:
        ordering = ['address']
        app_label = 'ipam'
        unique_together = [['address']]
