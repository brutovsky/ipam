from django.core.exceptions import ValidationError
from django.db import models
from netaddr import AddrFormatError, IPNetwork

from . import validators
from .formfields import IPNetworkFormField


class BaseIPField(models.Field):

    def python_type(self):
        return IPNetwork

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if not value:
            return value
        try:
            return IPNetwork(value)
        except AddrFormatError:
            raise ValidationError("Invalid IP address format: {}".format(value))
        except (TypeError, ValueError) as e:
            raise ValidationError(e)

    def get_prep_value(self, value):
        if not value:
            return None
        if isinstance(value, list):
            return [str(self.to_python(v)) for v in value]
        return str(self.to_python(value))

    def form_class(self):
        return IPNetworkFormField

    def formfield(self, **kwargs):
        defaults = {'form_class': self.form_class()}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class IPNetworkField(BaseIPField):
    """
    IP prefix (network and mask)
    """
    description = "PostgreSQL CIDR field"
    default_validators = [validators.prefix_validator]

    def db_type(self, connection):
        return 'cidr'


class IPAddressField(BaseIPField):
    """
    IP address (host address and mask)
    """
    description = "PostgreSQL INET field"

    def db_type(self, connection):
        return 'inet'
