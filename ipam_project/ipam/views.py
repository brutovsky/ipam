from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render


# Create your views here.


def ipam_component(request):

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
        'selected_option':selected_option,
        'model_pk': model_pk
    })
