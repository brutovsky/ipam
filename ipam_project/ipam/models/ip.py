from django.db import models
from ipam.choices import IPAddressStatusChoices, IPPrefixStatusChoices
from ipam.fields import IPAddressField, IPNetworkField
from ipam import validators
from ipam.models.vlan import VLAN


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
# IPAddress
#

class IPAddress(models.Model):
    address = IPAddressField(
        help_text='IPv4 or IPv6 address (with mask)'
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
        blank=True,
        validators=[validators.DNSValidator],
        verbose_name='DNS Name',
        help_text='Hostname'
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return str(self.address)

    class Meta:
        ordering = ['address']
        app_label = 'ipam'


#
# IPPrefixes
#

class IPPrefix(models.Model):
    prefix = IPNetworkField(
        help_text='IPv4 or IPv6 network with mask'
    )
    vlan = models.ForeignKey(
        VLAN,
        related_name='ip_prefixes',
        on_delete=models.PROTECT,
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

    def __str__(self):
        return str(self.prefix)

    class Meta:
        ordering = ['prefix']
        app_label = 'ipam'