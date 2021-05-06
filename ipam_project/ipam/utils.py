from django.db.models import ManyToManyField
from netaddr import IPSet
from rest_framework import serializers


class ValidatedModelSerializer(serializers.ModelSerializer):
    """
    Custom ModelSerializer that calls full_clean on the data
    """
    def validate(self, data):

        attrs = data.copy()

        # Skip ManyToManyFields
        for field in self.Meta.model._meta.get_fields():
            if isinstance(field, ManyToManyField):
                attrs.pop(field.name, None)

        # Run clean() on an instance of the model
        if self.instance is None:
            instance = self.Meta.model(**attrs)
        else:
            instance = self.instance
            for k, v in attrs.items():
                setattr(instance, k, v)
        instance.full_clean()

        if isinstance(instance, AttributeGenerator):
            for (attr_name, attr_val) in instance.attrs():
                data[attr_name] = attr_val

        return data


class AttributeGenerator:
    def attrs(self):
        for field in self._meta.fields:
            yield field.name, getattr(self, field.name)


def toset(ipprefix):
    return IPSet([ipprefix.prefix])


def calc_ipaddress_children(subnets):
    result = 0
    for subnet in subnets:
        if subnet.is_container:
            result += calc_ipaddress_children(subnet.subnets.all())
        else:
            child_count = IPSet([ip.address.ip for ip in subnet.ip_addresses.all()]).size
            if subnet.prefix.version == 4 and subnet.prefix.prefixlen < 31 and not subnet.is_pool:
                child_count += 2
            result += child_count
    return result
