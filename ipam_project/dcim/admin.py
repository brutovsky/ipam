from django.contrib import admin
from .models.site import *
from .models.rack import *

# Register your models here.

admin.site.register(Region)
admin.site.register(Site)

admin.site.register(RackGroup)
admin.site.register(RackRole)
admin.site.register(Rack)
