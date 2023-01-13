from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm,  UserAuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()


def user_login(request):
  context = {}
  user = request.user
  if user.is_authenticated:
    return redirect('home')

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


def user_logout(request):
    logout(request)
    messages.success(request, ("User Logged Out!"))
    
    # change to redirect to page user logged out on
    return redirect('home')

def register_user(request):
    context = {}
    if request.method == "POST":
      form = UserRegistrationForm(request.POST)
      messages.success(request, ("I Got to here 1"))
      if form.is_valid():
        #user = form.save()
        #user.set_password(user.password)
        form.save()

        Email = form.cleaned_data.get('Email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(Email=Email, password=raw_password)
        messages.success(request, (Email, raw_password))
        messages.success(request, (user))
        login(request, user)

        messages.success(request, ("Registration Successful! Password"))
        return redirect('home')
      else:
        context['UserRegistrationForm'] = form
    else:
      form = UserRegistrationForm()
      context['UserRegistrationForm'] = form

    return render(request, 'authentication/register_user.html', context)