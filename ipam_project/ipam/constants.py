#
# IPAddresses
#

IPADDRESS_MASK_LENGTH_MIN = 1
IPADDRESS_MASK_LENGTH_MAX = 128  # IPv6


#
# Prefixes
#

PREFIX_LENGTH_MIN = 1
PREFIX_LENGTH_MAX = 127  # IPv6


#
# VLANs
#

# 12-bit VLAN ID (values 0 and 4095 are reserved)
VLAN_VID_MIN = 1
VLAN_VID_MAX = 4094


#
# Services
#

# 16-bit port number
SERVICE_PORT_MIN = 1
SERVICE_PORT_MAX = 65535