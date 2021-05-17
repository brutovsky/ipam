from django.contrib import admin
from .models.locations import *
from .models.racks import *
from .models.devices import *


admin.site.register(Region)
admin.site.register(Location)

admin.site.register(RackGroup)
admin.site.register(RackRole)
admin.site.register(Rack)

admin.site.register(Manufacturer)
admin.site.register(Platform)
admin.site.register(DeviceType)
admin.site.register(DeviceRole)
admin.site.register(Device)
