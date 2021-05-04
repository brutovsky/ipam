from django.core.exceptions import ValidationError
from django.db import models
from ipam.choices import IPAddressStatusChoices, IPPrefixStatusChoices
from ipam.fields import IPAddressField, IPNetworkField
from ipam import validators
from ipam.models.vlan import VLAN
from dcim.models.locations import Location
from netaddr import IPNetwork, IPSet
from ipam.utils import toset, AttributeGenerator


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

class IPPrefix(models.Model, AttributeGenerator):
    prefix = IPNetworkField(
        help_text='IPv4 or IPv6 network with mask'
    )
    is_container = models.BooleanField(
        verbose_name='Is a container',
        default=False,
        help_text='Other IP prefixes can be nested inside this prefix'
    )
    prefix_container = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'is_container': True},
        help_text='Choose prefix container if this prefix is nested',
        related_name='subnets'
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
        print(self.pk)
        # Container constraints and validation
        if self.is_container:
            self.vlan = None
            self.is_pool = False
            self.location = None

        # Prefix constraints and validation
        else:
            # Check if this prefix has any subnets
            subnets_quantity = len(self.subnets.all())
            if subnets_quantity > 0:
                raise ValidationError(
                    f'{self.prefix} MUST be container, {subnets_quantity} subnets found')
            # Check if this prefix has location
            if not self.location:
                raise ValidationError(
                    f'{"Pool" if self.is_pool else "Default"} {self.prefix} prefix MUST be assigned to location')

        subnet = IPSet([self.prefix])

        # Validation of subnet prefix
        if self.prefix and self.prefix_container:
            print(self.prefix_container.location)
            # Check if the prefix is subnet of container
            container = IPSet([self.prefix_container.prefix])
            if not container > subnet:
                raise ValidationError(f'{subnet} is not subnet of {container}')
            # Check if the prefix doesn`t overlap with other subnets
            container_children = map(toset, IPPrefix.objects.filter(prefix_container=self.prefix_container).exclude(pk=self.pk))
            for child in container_children:
                if len(child & subnet) != 0:
                    raise ValidationError(f'{subnet} overlaps with {child}')
            #
            if self.location and self.prefix_container.location and self.location != self.prefix_container.location:
                raise ValidationError(f'{self.prefix} prefix`s location doesn`t match with its container`s')

        # Validation of root prefix
        else:
            if self.is_container:
                root_prefixes = IPPrefix.objects.filter(prefix_container=None).exclude(pk=self.pk)
                all_ip_sets = map(toset, root_prefixes)
            else:
                all_ip_sets = map(toset, IPPrefix.objects.all().exclude(pk=self.pk))
            # Check if the prefix overlaps with other prefixes
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

class IPAddress(models.Model, AttributeGenerator):
    address = IPAddressField(
        help_text='IPv4 or IPv6 address (with mask)'
    )
    prefix = models.ForeignKey(
        IPPrefix,
        related_name='ip_addresses',
        on_delete=models.CASCADE,
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
    assigned_service = models.ForeignKey(
        to='ipam.service',
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

        if self.assigned_service and self.assigned_interface and self.assigned_service.device != self.assigned_interface.device:
            raise ValidationError(f'{self.assigned_interface} doesn`t belong to {self.assigned_service} service`s device interfaces(try to change {self.address} interface assignment)')

    def __str__(self):
        return str(f'{f"{self.dns_name}:" if self.dns_name else ""}{self.address}')

    class Meta:
        ordering = ['address']
        app_label = 'ipam'
        unique_together = [['address']]
