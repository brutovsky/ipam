from django.contrib import admin
from .models.site import Region, Site

# Register your models here.

admin.site.register(Region)
admin.site.register(Site)
