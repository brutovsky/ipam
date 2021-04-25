from django.contrib import admin
from .models.site import *
from .models.rack import *
from .models.device import *

# Register your models here.

admin.site.register(Region)
admin.site.register(Site)

admin.site.register(RackGroup)
admin.site.register(RackRole)
admin.site.register(Rack)

admin.site.register(Manufacturer)
admin.site.register(Platform)
admin.site.register(DeviceType)
admin.site.register(DeviceRole)
admin.site.register(Device)
