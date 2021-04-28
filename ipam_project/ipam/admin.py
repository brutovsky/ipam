from django.contrib import admin
from .models.ip import *
from .models.vlan import *

# Register your models here.

admin.site.register(IPRole)
admin.site.register(IPAddress)
admin.site.register(IPPrefix)

admin.site.register(VLANRole)
admin.site.register(VLANGroup)
admin.site.register(VLAN)
