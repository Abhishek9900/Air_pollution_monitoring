try:
    from urllib.parse import quote_plus
except:
    pass
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from . import forms
from .models import Profile
import os


def delete_profile_image(filename,user):
    file_name = "{}_{}".format(user,filename)
    os.remove(settings.MEDIA_ROOT+'/'+filename)


@login_required
def profile(request):
    profile = request.user.profile.get()
    return render(request, 'accounts/profile.html',{'profile':profile})


@login_required
def edit_profile(request):
    profile = request.user.profile.get()
    form = forms.EditProfileForm(instance=profile)
    if request.method =='POST':
        form = forms.EditProfileForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            try:
                form.save(request.user)
                messages.success(request, 'Profile edited successfully')
                return HttpResponseRedirect(reverse('home'))
            except Exception as e:
                messages.danger(request, 'Error editing profile: {}'.format(e))
                return HttpResponseRedirect(reverse('accounts:edit_profile'))
    return render(request, 'accounts/edit_profile.html',{'form':form,
                            'profile':profile})


@login_required
def edit_profile_pic(request):
    profile = request.user.profile.get()
    # keep a hold of the old image
    old_image = profile.image.name
    form = forms.EditProfilepicForm(instance=profile)
    if request.method =='POST':
        form = forms.EditProfilepicForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            try:
                delete_profile_image(old_image,request.user)
                form.save(request.user)
                messages.success(request, 'Profile pic edited successfully')
                return HttpResponseRedirect(reverse('home'))
            except Exception as e:
                messages.danger(request, 'Error editing profile pic: {}'.format(e))
                return HttpResponseRedirect(reverse('accounts:edit_profile_pic'))
    return render(request, 'accounts/edit_profile_pic.html',{'form':form,
                            'profile':profile})

@login_required
def create_profile(request):
    form = forms.UserProfileForm()
    if request.method =='POST':
        form = forms.UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                profile = form.save(request.user)
                messages.success(request, 'Profile created successfully')
                return HttpResponseRedirect(reverse('home'))
            except Exception as e:
                messages.danger(request, 'Error creating profile: {}'.format(e))
                return HttpResponseRedirect(reverse('accounts:create_profile'))
    return render(request, 'accounts/create_profile.html',{'form':form})


@login_required
def change_password(request):
    form = forms.ChangePasswordForm(request.user)
    if request.method=='POST':
        form = forms.ChangePasswordForm(request.user,request.POST)
        if form.is_valid():
            try:
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                messages.success(request, 'Password changed successfully')
                return HttpResponseRedirect(reverse('home'))
            except Exception as e:
                messages.danger(request, 'Error changing password: {}'.format(e))
                return HttpResponseRedirect(reverse('accounts:change_password'))
    return render(request, 'accounts/change_password.html',{'form':form})


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    if request.user.profile.all().count():
                        return HttpResponseRedirect(
                            reverse('home')
                        )
                    else:
                        return HttpResponseRedirect(
                                    reverse('accounts:create_profile')
                                    ) # TODO: go to profile
                else:
                    messages.danger(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.danger(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))