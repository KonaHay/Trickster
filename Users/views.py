from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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
    return redirect('home')

# ======================================================================================================================================

def register_user(request):
    context = {}
    if request.method == "POST":
      form = UserRegistrationForm(request.POST)
      if form.is_valid():
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

@login_required(login_url='login')
def profile(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)

    current_page = request.path
    return render(request, 'user_pages/profile.html', {'profile': profile, 'current_page':current_page})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

@login_required(login_url='login')
def update_profile(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)
    user = Trickster_User.objects.get(UserID=pk)

    if request.method == 'POST':
      user_form = UserUpdateForm(request.POST or None, instance=user)
      profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
      
      if profile_form.is_valid() and user_form.is_valid():
        profile_form.save()
        user_form.save()
        messages.success(request, ("Account Updated Successfully!"))
        return HttpResponseRedirect('/Users/profile/%d'%user.UserID)
      
    else:
      profile_form = ProfileUpdateForm(instance=profile)
      user_form = UserUpdateForm(instance=user)
    return render(request, 'user_pages/update_profile.html', {'profile':profile, 'profile_form':profile_form, 'user_form':user_form})

  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

@login_required(login_url='login')
def my_tricks(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)
    trick_count = profile.LearnedTricks.all().count()
    tricks = profile.LearnedTricks.order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

    current_page = request.path
    return render(request, 'user_pages/my_tricks.html', {'profile': profile, 'tricks':tricks, "trick_count":trick_count, 'current_page':current_page})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

@login_required(login_url='login')
def my_completed_programmes(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)
    programmes = profile.CompletedProgrammes.order_by('ProgrammeRecLevel', 'ProgrammeDifficulty', 'ProgrammeName')

    return render(request, 'user_pages/my_completed_programmes.html', {'profile': profile, 'programmes':programmes})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')
  
# ======================================================================================================================================

@login_required(login_url='login')
def my_saved_tricks(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)
    trick_count = profile.SavedTricks.all().count()

    current_page = request.path
    return render(request, 'user_pages/my_saved_tricks.html', {'profile': profile, "trick_count":trick_count, 'current_page':current_page})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

@login_required(login_url='login')
def my_saved_programmes(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)
    programme_count = profile.SavedProgrammes.all().count()

    current_page = request.path
    return render(request, 'user_pages/my_saved_programmes.html', {'profile': profile, "programme_count":programme_count, 'current_page':current_page})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')

# ======================================================================================================================================

@login_required(login_url='login')
def my_skill_level(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)

    current_page = request.path
    return render(request, 'user_pages/my_skill_level.html', {'profile': profile, 'current_page':current_page})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')
  
# ======================================================================================================================================

@login_required(login_url='login')
def following(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)

    current_page = request.path
    return render(request, 'user_pages/following.html', {'profile': profile, 'current_page':current_page})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')
  
# ======================================================================================================================================

@login_required(login_url='login')
def followers(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)

    current_page = request.path
    return render(request, 'user_pages/followers.html', {'profile': profile, 'current_page':current_page})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')
  
# ======================================================================================================================================

@login_required(login_url='login')
def follow(request, pk):
  userProfile = User_Profile.objects.get(User_id=pk)
  Profile = get_object_or_404(User_Profile, User=request.POST.get("profile_id"))
  userProfile.Follows.add(Profile)

  current_page = request.POST.get("current_page")
  messages.info(request, ("You have followed " + Profile.User.Username + "!"))
  return redirect(current_page)

# ======================================================================================================================================

@login_required(login_url='login')
def unfollow(request, pk):
  userProfile = User_Profile.objects.get(User_id=pk)
  Profile = get_object_or_404(User_Profile, User=request.POST.get("profile_id"))
  userProfile.Follows.remove(Profile)

  current_page = request.POST.get("current_page")
  messages.error(request, ("You have unfollowed " + Profile.User.Username + "!"))
  return redirect(current_page)