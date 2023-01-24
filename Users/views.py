from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import  Trickster_User, User_Profile
from .forms import UserRegistrationForm,  UserAuthenticationForm, ProfileUpdateForm
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
        return redirect('home')

  else:
    form = UserAuthenticationForm()

  context['user_login'] = form
  return render(request, 'authentication/login.html', context)

# ======================================================================================================================================

def user_logout(request):
    logout(request)
    messages.success(request, ("User Logged Out!"))
    
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
    messages.success(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

def update_profile(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
      form.save()
      messages.success(request, ("The Changes To Your Profile Have Been Saved!"))
      return redirect('home')
  else:
    messages.success(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')
  return render(request, 'user_pages/update_profile.html', {'profile':profile, 'form':form})

# ======================================================================================================================================

def my_tricks(request, pk):
  if request.user.is_authenticated:

    profile = User_Profile.objects.get(User_id=pk)

    return render(request, 'user_pages/my_tricks.html', {'profile': profile})
  else:
    messages.success(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

def my_saved_tricks(request, pk):
  if request.user.is_authenticated:

    profile = User_Profile.objects.get(User_id=pk)

    return render(request, 'user_pages/my_saved_tricks.html', {'profile': profile})
  else:
    messages.success(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')