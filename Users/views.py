from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
    return redirect('home')