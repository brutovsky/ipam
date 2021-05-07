from braces.views import PermissionRequiredMixin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from ipam.models.ip import IPPrefix


# Create your views here.


def ipam_component(request):
    response = redirect('/ipam/ipam-logs')
    return response


def ipam_logs(request):
    if request.method == 'GET' and 'model' in request.GET:
        model = request.GET['model']
    else:
        model = 'ipaddress'

    select_options = ContentType.objects.filter(app_label="ipam")
    selected_option = model
    ipam_model = ContentType.objects.get(app_label="ipam", model=model)
    model_pk = ipam_model.pk
    logs = LogEntry.objects.filter(content_type=ipam_model).order_by('-action_time')[:10]

    return render(request, 'ipam/ipam-component.html', {
        'logs': logs,
        'select_options': select_options,
        'selected_option': selected_option,
        'model_pk': model_pk
    })


class PrefixListView(PermissionRequiredMixin, ListView):
    model = IPPrefix
    template_name = 'ipam/prefix-list.html'
    context_object_name = 'prefixes'
    permission_required = "ipam.view_ipprefix"


class PrefixDetailView(PermissionRequiredMixin, DetailView):
    model = IPPrefix
    template_name = 'ipam/prefix-detail.html'
    permission_required = "ipam.view_ipprefix"


class PrefixChildrenView(PermissionRequiredMixin, View):
    permission_required = 'ipam.view_ipprefix'

    def get(self, request, *args, **kwargs):
        prefix = get_object_or_404(IPPrefix, pk=kwargs['pk'])
        prefix_children = prefix.subnets.all()
        return render(request, 'ipam/prefix-children.html', {
            'object': prefix,
            'children': prefix_children
        })


class PrefixIpAddressesView(PermissionRequiredMixin, View):
    permission_required = 'ipam.view_ipaddress'

    def get(self, request, *args, **kwargs):
        prefix = get_object_or_404(IPPrefix, pk=kwargs['pk'])
        prefix_ips = prefix.ip_addresses.all()
        prefix_available_ips = prefix.get_available_ips()
        return render(request, 'ipam/prefix-ip-addresses.html', {
            'object': prefix,
            'ipaddresses': prefix_ips,
            'available_iprange': list(prefix_available_ips.iter_ipranges())
        })
