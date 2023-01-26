from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import  Trickster_User, User_Profile
from .forms import UserRegistrationForm,  UserAuthenticationForm, ProfileUpdateForm, UserUpdateForm
from TricksterMain.models import Trick, SkillLevel

# ======================================================================================================================================

def user_login(request):
  context = {}
  user = request.user
  if user.is_authenticated:
    return HttpResponseRedirect('home')

  if request.method == "POST":
    form = UserAuthenticationForm(request.POST)
    if form.is_valid():
      Email = request.POST['Email']
      password = request.POST['password']
      user = authenticate(Email=Email, password=password)

      if user is not None:
        login(request, user)
        messages.success(request, ("Login Successful!"))
        return redirect('home')
    context['UserAuthenticationForm'] = form
  else:
    form = UserAuthenticationForm()
    context['UserAuthenticationForm'] = form

  context['user_login'] = form
  return render(request, 'authentication/login.html', context)

# ======================================================================================================================================

def user_logout(request):
    logout(request)
    messages.warning(request, ("User Logged Out!"))
    
    # change to redirect to page user logged out on
    return redirect('home')

# ======================================================================================================================================

def register_user(request):
    context = {}
    if request.method == "POST":
      form = UserRegistrationForm(request.POST)
      if form.is_valid():
        #user = form.save()
        #user.set_password(user.password)
        form.save()

        Email = form.cleaned_data.get('Email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(Email=Email, password=raw_password)
        login(request, user)

        messages.success(request, ("Registration Successful!"))
        return redirect('home')
      else:
        context['UserRegistrationForm'] = form
    else:
      form = UserRegistrationForm()
      context['UserRegistrationForm'] = form

    return render(request, 'authentication/register_user.html', context)

# ======================================================================================================================================

def profile(request, pk):
  if request.user.is_authenticated:

    profile = User_Profile.objects.get(User_id=pk)

    return render(request, 'user_pages/profile.html', {'profile': profile})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

def update_profile(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)
    user = Trickster_User.objects.get(UserID=pk)

    if request.method == 'POST':

      if 'UpdateProfile' in request.POST:
        profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
        if profile_form.is_valid():
          profile_form.save()
          messages.success(request, ("The Changes To Your Profile Have Been Saved!"))
          return HttpResponseRedirect('/Users/profile/%d'%user.UserID)

      elif 'UpdateUser' in request.POST:
        user_form = UserUpdateForm(request.POST or None, instance=user)
        if user_form.is_valid():
          user_form.save()
          messages.success(request, ("The Changes To Your Profile Have Been Saved!"))
          return HttpResponseRedirect('/Users/profile/%d'%user.UserID)

    profile_form = ProfileUpdateForm(instance=profile)
    user_form = UserUpdateForm(instance=user)
    return render(request, 'user_pages/update_profile.html', {'profile':profile, 'profile_form':profile_form, 'user_form':user_form})

  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

def my_tricks(request, pk):
  if request.user.is_authenticated:

    profile = User_Profile.objects.get(User_id=pk)
    trick_count = profile.LearnedTricks.all().count()

    return render(request, 'user_pages/my_tricks.html', {'profile': profile, "trick_count":trick_count})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

def my_saved_tricks(request, pk):
  if request.user.is_authenticated:

    profile = User_Profile.objects.get(User_id=pk)
    trick_count = profile.SavedTricks.all().count()

    return render(request, 'user_pages/my_saved_tricks.html', {'profile': profile, "trick_count":trick_count})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')