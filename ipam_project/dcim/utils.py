from netaddr import IPSet


def toset(ipprefix):
    return IPSet([ipprefix.prefix])