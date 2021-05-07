from braces.views import PermissionRequiredMixin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from ipam.models.ip import IPPrefix, IPAddress


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


class PrefixLogsView(PermissionRequiredMixin, View):
    permission_required = 'admin.view_logentry'

    def get(self, request, *args, **kwargs):
        prefix = get_object_or_404(IPPrefix, pk=kwargs['pk'])
        prefix_model = ContentType.objects.get(app_label="ipam", model="ipprefix")
        model_pk = prefix_model.pk
        logs = LogEntry.objects.filter(content_type=prefix_model, object_id=prefix.pk).order_by('-action_time')[:10]

        return render(request, 'ipam/prefix-logs.html', {
            'object': prefix,
            'logs': logs,
            'model_pk': model_pk
        })


#
# IPAddress views
#

class IPAddressListView(PermissionRequiredMixin, ListView):
    model = IPAddress
    template_name = 'ipam/ipaddress/ipaddress-list.html'
    context_object_name = 'ipaddresses'
    permission_required = "ipam.view_ipaddress"


class IPAddressDetailView(PermissionRequiredMixin, DetailView):
    model = IPAddress
    template_name = 'ipam/ipaddress/ipaddress-detail.html'
    permission_required = "ipam.view_ipaddress"


class IPAddressLogsView(PermissionRequiredMixin, View):
    permission_required = 'admin.view_logentry'

    def get(self, request, *args, **kwargs):
        ipaddress = get_object_or_404(IPAddress, pk=kwargs['pk'])
        ipaddress_model = ContentType.objects.get(app_label="ipam", model="ipaddress")
        model_pk = ipaddress_model.pk
        logs = LogEntry.objects.filter(content_type=ipaddress_model, object_id=ipaddress.pk).order_by('-action_time')[
               :10]

        return render(request, 'ipam/ipaddress/ipaddress-logs.html', {
            'object': ipaddress,
            'logs': logs,
            'model_pk': model_pk
        })
