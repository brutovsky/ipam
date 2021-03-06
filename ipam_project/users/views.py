from braces.views import StaffuserRequiredMixin, SuperuserRequiredMixin, PermissionRequiredMixin
from django.contrib.admin.models import LogEntry
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import *

from .forms import UserRegisterForm, UserProfileForm, ChangePasswordForm
import django.contrib.auth.password_validation as validators


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile has been successfully updated')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():

            if not request.user.check_password(form.cleaned_data['old_password']):
                messages.error(request, f'Wrong password', extra_tags='danger')
                return redirect('change-password')

            try:
                validators.validate_password(password=form.cleaned_data['new_password'])
            except ValidationError as e:
                messages.error(request, f'{"".join(e.messages)}', extra_tags='danger')
                return redirect('change-password')

            if form.cleaned_data["new_password"] != form.cleaned_data['new_password_repeat']:
                messages.error(request, f'Passwords doesn`t match', extra_tags='danger')
                return redirect('change-password')

            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            messages.success(request, f'Password has been successfully updated')
            return redirect('profile')
    else:
        form = ChangePasswordForm()

    return render(request, 'users/change-password.html', {'form': form})


class UserListView(StaffuserRequiredMixin, SuperuserRequiredMixin,  ListView):
    model = User
    template_name = 'users/user-list.html'
    context_object_name = 'users'


class GroupListView(StaffuserRequiredMixin, SuperuserRequiredMixin,  ListView):
    model = Group
    template_name = 'users/group-list.html'
    context_object_name = 'groups'


def user_component(request):
    response = redirect('/users/users-logs')
    return response


@permission_required('admin.view_logentry')
def users_logs(request):
    if request.method == 'GET' and 'model' in request.GET:
        model = request.GET['model']
    else:
        model = 'user'

    select_options = ContentType.objects.filter(app_label="auth")
    selected_option = model
    auth_model = ContentType.objects.get(app_label="auth", model=model)
    model_pk = auth_model.pk
    logs = LogEntry.objects.filter(content_type=auth_model).order_by('-action_time')[:10]

    return render(request, 'users/user-component.html', {
        'logs': logs,
        'select_options': select_options,
        'selected_option':selected_option,
        'model_pk': model_pk
    })





