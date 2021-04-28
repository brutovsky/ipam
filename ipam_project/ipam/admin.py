from django.contrib import admin
from .models.ip import *

# Register your models here.

admin.site.register(IPRole)
admin.site.register(IPAddress)
admin.site.register(IPPrefix)
