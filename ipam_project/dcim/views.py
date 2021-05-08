from braces.views import PermissionRequiredMixin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.views.generic import ListView
from dcim.models import Region, Location


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