import netaddr
from django.core.exceptions import ValidationError
from django.db import models
from ipam.choices import IPAddressStatusChoices, IPPrefixStatusChoices
from ipam.fields import IPAddressField, IPNetworkField
from ipam import validators
from ipam.models.vlan import VLAN
from dcim.models.locations import Location
from netaddr import IPNetwork, IPSet
from ipam.utils import toset, AttributeGenerator
from ipam.utils import calc_ipaddress_children

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

    @property
    def family(self):
        if self.prefix:
            return self.prefix.version
        return None

    def get_utilization(self):
        """
        Determine the utilization of the prefix and return it as a percentage.
        For container, calculate utilization based on subnet prefixes.
        For all others, count child IP addresses.
        """
        if self.is_container:
            child_count = calc_ipaddress_children(self.subnets.all())
            return round(float(child_count) / self.prefix.size * 100, 2)
        else:
            child_count = IPSet([ip.address.ip for ip in self.ip_addresses.all()]).size
            prefix_size = self.prefix.size
            if self.prefix.version == 4 and self.prefix.prefixlen < 31 and not self.is_pool:
                prefix_size -= 2
            return round(float(child_count) / prefix_size * 100, 2)

    def get_available_ips(self):
        """
        Return all available IPs within this prefix as an IPSet.
        """
        prefix = IPSet(self.prefix)

        if self.is_container and self.subnets:
            available_ips = IPSet([])
            for subnet in self.subnets.all():
                available_ips.update(subnet.get_available_ips())
            return available_ips

        prefix_ips = IPSet([ip.address.ip for ip in self.ip_addresses.all()])
        available_ips = prefix - prefix_ips

        # IPv6, pool, or IPv4 /31 sets are fully usable
        if self.family == 6 or self.is_pool or self.prefix.prefixlen == 31:
            return available_ips

        # For "normal" IPv4 prefixes, omit first and last addresses
        available_ips -= IPSet([
            netaddr.IPAddress(self.prefix.first),
            netaddr.IPAddress(self.prefix.last),
        ])

        return available_ips

    # def get_ip_addresses_with_available(self):
    #     all_addresses = IPSet([self.prefix])
    #     ip_addresses = IPSet([ip.address.ip for ip in self.ip_addresses.all()])
    #     all_addresses -

    def clean(self):
        super().clean()
        print(self.pk)
        # Container constraints and validation
        if self.is_container:
            self.vlan = None
            self.is_pool = False
            self.location = None

            ipaddresses_quantity = len(self.ip_addresses.all())
            if ipaddresses_quantity > 0:
                raise ValidationError(
                    f'{self.prefix} can not be container, {ipaddresses_quantity} bound ip addresses found')

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
            # Validate VLANGroup location
            if self.vlan and self.vlan.vlan_group.location != self.location:
                raise ValidationError(
                    f'VLAN Group "{self.vlan.vlan_group}" location mismatch with prefix {self.prefix} location -> {self.vlan.vlan_group.location}|{self.location}')

        subnet = IPSet([self.prefix])

        # Validation of subnet prefix
        if self.prefix and self.prefix_container:
            print(self.prefix_container.location)
            # Check if the prefix family matches with container`s
            if self.prefix_container.family != self.family:
                raise ValidationError(
                    f'Prefix {self.prefix} protocol mismatch with prefix {self.prefix_container} protocol -> IPv{self.family}|IPv{self.prefix_container.family}')
            # Check if the prefix is subnet of container
            container = IPSet([self.prefix_container.prefix])
            if not container > subnet:
                raise ValidationError(f'{subnet} is not subnet of {container}')
            # Check if the prefix doesn`t overlap with other subnets
            container_children = map(toset, IPPrefix.objects.filter(prefix_container=self.prefix_container).exclude(
                pk=self.pk))
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
        # dns-name to lower case
        if hasattr(self, 'dns_name') and self.dns_name:
            self.dns_name = self.dns_name.lower()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        # IP address prefix validation
        if self.address and hasattr(self, 'prefix'):
            if self.address.prefixlen == 0:
                raise ValidationError({
                    'address': "Cannot create IP address with /0 mask."
                })
            if IPNetwork(self.address) != self.prefix.prefix:
                raise ValidationError('IP Address network and prefix does not match')
        # Verify that dns name is unique
        all_ip_addresses = IPAddress.objects.all().exclude(pk=self.pk)
        for ip_address in all_ip_addresses:
            if self.dns_name and self.dns_name == ip_address.dns_name:
                raise ValidationError(f'{self.address} dns name already exist')
        # Validate service assignment
        if self.assigned_service and self.assigned_interface and self.assigned_service.device != self.assigned_interface.device:
            raise ValidationError(
                f'{self.assigned_interface} doesn`t belong to {self.assigned_service} service`s device interfaces(try to change {self.address} interface assignment)')

    def __str__(self):
        return str(f'{f"{self.dns_name}:" if self.dns_name else ""}{self.address}')

    class Meta:
        ordering = ['address']
        app_label = 'ipam'
        unique_together = [['address']]
