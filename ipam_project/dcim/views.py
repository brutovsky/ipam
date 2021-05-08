from braces.views import PermissionRequiredMixin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from dcim.models.locations import Region, Location
from dcim.models.racks import RackGroup, RackRole, Rack
from dcim.models.devices import *


def dcim_component(request):
    response = redirect('/dcim/dcim-logs')
    return response


def dcim_logs(request):
    if request.method == 'GET' and 'model' in request.GET:
        model = request.GET['model']
    else:
        model = 'device'

    select_options = ContentType.objects.filter(app_label="dcim")
    selected_option = model
    dcim_model = ContentType.objects.get(app_label="dcim", model=model)
    model_pk = dcim_model.pk
    logs = LogEntry.objects.filter(content_type=dcim_model).order_by('-action_time')[:10]

    return render(request, 'dcim/dcim-component.html', {
        'logs': logs,
        'select_options': select_options,
        'selected_option': selected_option,
        'model_pk': model_pk
    })


#
# Region views
#


class RegionListView(PermissionRequiredMixin, ListView):
    model = Region
    template_name = 'dcim/region/region-list.html'
    context_object_name = 'regions'
    permission_required = "dcim.view_region"


#
# Location views
#

class LocationListView(PermissionRequiredMixin, ListView):
    model = Location
    template_name = 'dcim/location/location-list.html'
    context_object_name = 'locations'
    permission_required = "dcim.view_location"


class LocationDetailView(PermissionRequiredMixin, DetailView):
    model = Location
    template_name = 'dcim/location/location-detail.html'
    permission_required = "ipam.view_location"


class LocationRackGroupsView(PermissionRequiredMixin, View):
    permission_required = 'ipam.view_rackgroup'

    def get(self, request, *args, **kwargs):
        location = get_object_or_404(Location, pk=kwargs['pk'])
        rackgroups = location.rack_groups.all()
        return render(request, 'dcim/location/location-rackgroups.html', {
            'object': location,
            'rackgroups': rackgroups
        })


class LocationPrefixesView(PermissionRequiredMixin, View):
    permission_required = 'ipam.view_ipprefix'

    def get(self, request, *args, **kwargs):
        location = get_object_or_404(Location, pk=kwargs['pk'])
        prefixes = location.ip_prefixes.all()
        return render(request, 'dcim/location/location-prefixes.html', {
            'object': location,
            'prefixes': prefixes
        })

#
# RackGroup views
#

class RackGroupListView(PermissionRequiredMixin, ListView):
    model = RackGroup
    template_name = 'dcim/rackgroup/rackgroup-list.html'
    context_object_name = 'rackgroups'
    permission_required = "dcim.view_rackgroup"


#
# RackRole views
#

class RackRoleListView(PermissionRequiredMixin, ListView):
    model = RackRole
    template_name = 'dcim/rackrole/rackrole-list.html'
    context_object_name = 'rackroles'
    permission_required = "dcim.view_rackrole"


#
# Rack views
#

class RackListView(PermissionRequiredMixin, ListView):
    model = Rack
    template_name = 'dcim/rack/rack-list.html'
    context_object_name = 'racks'
    permission_required = "dcim.view_rack"


#
# Manufacturer views
#

class ManufacturerListView(PermissionRequiredMixin, ListView):
    model = Manufacturer
    template_name = 'dcim/manufacturer/manufacturer-list.html'
    context_object_name = 'manufacturers'
    permission_required = "dcim.view_manufacturer"


#
# Platform views
#

class PlatformListView(PermissionRequiredMixin, ListView):
    model = Platform
    template_name = 'dcim/platform/platform-list.html'
    context_object_name = 'platforms'
    permission_required = "dcim.view_platform"


#
# DeviceType views
#

class DeviceTypeListView(PermissionRequiredMixin, ListView):
    model = DeviceType
    template_name = 'dcim/devicetype/devicetype-list.html'
    context_object_name = 'devicetypes'
    permission_required = "dcim.view_devicetype"


#
# DeviceRole views
#

class DeviceRoleListView(PermissionRequiredMixin, ListView):
    model = DeviceRole
    template_name = 'dcim/devicerole/devicerole-list.html'
    context_object_name = 'deviceroles'
    permission_required = "dcim.view_devicerole"


#
# Device views
#

class DeviceListView(PermissionRequiredMixin, ListView):
    model = Device
    template_name = 'dcim/device/device-list.html'
    context_object_name = 'devices'
    permission_required = "dcim.view_device"
