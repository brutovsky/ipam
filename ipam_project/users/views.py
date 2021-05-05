from braces.views import StaffuserRequiredMixin, SuperuserRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .forms import UserRegisterForm, UserProfileForm, ChangePasswordForm
import django.contrib.auth.password_validation as validators


# Create your views here.


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


class UserListView(StaffuserRequiredMixin, SuperuserRequiredMixin, ListView):
    model = User
    template_name = 'users/users-list.html'
    context_object_name = 'users'

