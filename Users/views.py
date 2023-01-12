from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
            
        else:
            messages.success(request, ("Username Or Password Incorrect. Please Try Again."))
            return redirect('login')

    else:
        return render(request, 'authentication/login.html', {})

def user_logout(request):
    logout(request)
    messages.success(request, ("User Logged Out!"))
    
    # change to redirect to page user logged out on
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'authentication/register_user.html', {
        'form':form,
    })