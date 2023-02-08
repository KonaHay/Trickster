from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator

from random import shuffle

from .models import Trick, SkillLevel, Trick_Programme, Category
from .forms import TrickForm, ProgrammeForm, CategoryForm
from Users.models import Trickster_User, User_Profile 


def home(request):
  return render(request, 'main/home.html', {})

# ======================================================================================================================================

# ----------------------------------------------------------------------
# Attempt at a view based pagination setup
# class t_paginator(View):
#   tricks = Trick.objects.all().order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')
#   page_amount = 6
#   p = Paginator(tricks, page_amount)
  
#   def paginator_pages(self, request):   
#     page = request.GET.get('page')
#     trick_list = self.p.get_page(page)
#     num_pages = "T" * trick_list.paginator.num_pages
#     return HttpResponse({"num_pages":num_pages})

#   def paginator_tricks(self, request):
#     page = request.GET.get('page')
#     trick_list = self.p.get_page(page)

#     return HttpResponse({'trick_list': trick_list})
# ----------------------------------------------------------------------

# ======================================================================================================================================

def trick_list(request):
  #------ For view based paginator ---------
  #num_pages = t_paginator.paginator_pages
  #tricks = t_paginator.paginator_tricks
  #-----------------------------------------


  all_tricks = Trick.objects.all().order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')
  trick_count = all_tricks.count()

  #Pagination setup
  p = Paginator(all_tricks, 6)
  page = request.GET.get('page')
  tricks = p.get_page(page)
  num_pages = "T" * tricks.paginator.num_pages

  return render(request, 'main/trick_list.html', {'tricks': tricks, "num_pages":num_pages, "trick_count":trick_count})
   # -- Try replacing this link ^ to the paginator.html instead! --

# ======================================================================================================================================

# View for recommending tricks to users
def recommend_trick(request, pk):
  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)
    user_learned_tricks = profile.LearnedTricks
    user_skill_level = profile.SkillLevel
    user_ability = profile.UserDifficultyLevel

    learned_tricks = user_learned_tricks.order_by('TrickName')
    user_learned_trick_names = learned_tricks

    

    filters = models.Q()

    #Trying to filter by if the user has NOT learned the trick (~models.Q used to get Non Learned Tricks)
    #if user_learned_tricks: .exclude(TrickName__LearnedTricks=user_learned_trick_names)
    #filters &= ~models.Q(Trick__LearnedTricks=user_learned_tricks,)

    filters &= models.Q(TrickRecLevel=user_skill_level) & models.Q(TrickDifficulty=user_ability)

    recommend_tricks = Trick.objects.filter(filters).order_by('TrickName')
    messages.error(request, (learned_tricks))

    #Try to use paginator to put tricks into a carosel.


    return render(request, 'main/recommend_trick.html', {'recommend_tricks': recommend_tricks, 'profile': profile, 'user_learned_tricks':user_learned_tricks})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return HttpResponseRedirect('/home')

# ======================================================================================================================================

def random_trick(request):
  if request.method == "POST":

    randomised_tricks = Trick.objects.all().order_by('?')

    return render(request, 'main/random_trick.html', {'randomised_tricks':randomised_tricks,})
  else:
    return render(request, 'main/random_trick.html', {})

# ======================================================================================================================================

def random_trick_skill_based(request, pk):
  if request.user.is_authenticated:
    if request.method == "POST":
      profile = User_Profile.objects.get(User_id=pk)
      user_skill_level = profile.SkillLevel
      user_ability = profile.UserDifficultyLevel

      filters = models.Q()

      filters &= models.Q(TrickRecLevel=user_skill_level) & models.Q(TrickDifficulty=user_ability)

      random_trick = Trick.objects.filter(filters).order_by('?')

      return render(request, 'main/random_trick_skill_based.html', {'random_trick': random_trick, 'profile': profile,})
    else:
      return render(request, 'main/random_trick_skill_based.html', {})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return HttpResponseRedirect('/home')

# ======================================================================================================================================

def random_trick_learned(request, pk):
  if request.user.is_authenticated:
    if request.method == "POST":
      profile = User_Profile.objects.get(User_id=pk)
      user_learned_tricks = profile.LearnedTricks

      random_trick = user_learned_tricks.order_by('?')
      
      return render(request, 'main/random_trick_learned.html', {'random_trick': random_trick, 'profile': profile,})
    else:
      return render(request, 'main/random_trick_learned.html', {})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return HttpResponseRedirect('/home')

# ======================================================================================================================================

def learned_trick(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))
  profile.LearnedTricks.add(trick)

  messages.info(request, (trick.TrickName + " Has Been Added To Your List Of Learned Tricks!"))
  return HttpResponseRedirect('/home')
  #return HttpResponseRedirect(reverse('recommend-trick', args=[str(pk)]))

# ======================================================================================================================================

def unlearn_trick(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))

  if profile.LearnedTricks.filter(TrickID=trick.TrickID).exists():
    profile.LearnedTricks.remove(trick)

  messages.error(request, (trick.TrickName + " Has Been Removed From Your List Of Learned Tricks!"))
  return HttpResponseRedirect('/home')
  #return HttpResponseRedirect(reverse('recommend-trick', args=[str(pk)]))

# ======================================================================================================================================

def save_trick(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))
  profile.SavedTricks.add(trick)

  messages.info(request, (trick.TrickName + " Has Been Added To Your List Of Saved Tricks!"))
  return HttpResponseRedirect('/home')
  #return HttpResponseRedirect(reverse('recommend-trick', args=[str(pk)]))

# ======================================================================================================================================

def unsave_trick(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))

  if profile.SavedTricks.filter(TrickID=trick.TrickID).exists():
    profile.SavedTricks.remove(trick)

  messages.error(request, (trick.TrickName + " Has Been Removed From Your List Of Saved Tricks!"))
  return HttpResponseRedirect('/home')
  #return HttpResponseRedirect(reverse('recommend-trick', args=[str(pk)]))

# ======================================================================================================================================

@permission_required('trick.add_trick', login_url='home')
def add_trick(request):
    submitted = False
    if request.method == "POST":
      form = TrickForm(request.POST, request.FILES)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect('/add_trick?submitted=True')
    else:
      form = TrickForm
      if 'submitted' in request.GET:
        submitted = True
        messages.success(request, ("Trick Added Successfuly!"))
    return render(request, 'main/add_trick.html', {'form':form, 'submitted':submitted})

# ======================================================================================================================================

def show_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  return render(request, 'main/show_trick.html', {'trick' : trick})

# ======================================================================================================================================

@permission_required('trick.change_trick', login_url='home')
def update_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  form = TrickForm(request.POST or None, instance=trick)
  if form.is_valid():
    form.save()
    messages.success(request, ("Trick Updated Successfuly!"))
    return HttpResponseRedirect('/trick_list')
  return render(request, 'main/update_trick.html', {'trick':trick, 'form':form})

# ======================================================================================================================================

def search_trick(request):
  if request.method == "POST":
    trick_searched = request.POST['trick_searched']
    tricks =  Trick.objects.filter(TrickName__contains=trick_searched).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

    return render(request, 'main/search_trick.html', {'trick_searched':trick_searched, 'tricks':tricks})
  else:
    return render(request, 'main/search_trick.html', {})

# ======================================================================================================================================

@permission_required('trick.delete_trick', login_url='home')
def delete_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  trick.delete()
  return HttpResponseRedirect('/trick_list')

# ======================================================================================================================================

def trick_card(request, pk):

  return render(request, 'components/trick_cards.html', {})

# ======================================================================================================================================

@permission_required('trick.add_programme', login_url='home')
def add_programme(request):
    submitted = False
    if request.method == "POST":
      form = ProgrammeForm(request.POST, request.FILES)
      if form.is_valid():
        new_programme = form.save()
        #need to pass the ProgrammeID after its been created.
        programme = new_programme
        return HttpResponseRedirect('/add_programme_success/%d'%programme.ProgrammeID)
    else:
      form = ProgrammeForm
      if 'submitted' in request.GET:
        submitted = True
        messages.success(request, ("Trick Programme Added Successfully!"))
    return render(request, 'main/add_programme.html', {'form':form, 'submitted':submitted})


def add_programme_success(request, programme_id):
  Programme = Trick_Programme.objects.get(pk=programme_id)

  return render(request, 'main/add_programme_success.html', {'Programme':Programme})

# ======================================================================================================================================

@permission_required('trick.add_programme', login_url='home')
def add_programme_tricks_list(request, programme_id):

  all_tricks = Trick.objects.all().order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

  Programme = Trick_Programme.objects.get(pk=programme_id)
  Programme_Tricks = Programme.ProgrammeTricks.order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

  #Search Trick Function
  if request.method == "POST":
    trick_searched = request.POST['trick_searched']
    searched_tricks =  Trick.objects.filter(TrickName__contains=trick_searched).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

    return render(request, 'main/add_programme_tricks.html', {
      'Programme':Programme, 
      'Programme_Tricks':Programme_Tricks, 
      'all_tricks':all_tricks, 
      'trick_searched':trick_searched, 
      'searched_tricks':searched_tricks
      })
  else:
    return render(request, 'main/add_programme_tricks.html', {
    'Programme':Programme, 
    'Programme_Tricks':Programme_Tricks, 
    'all_tricks':all_tricks, 
    })

# ======================================================================================================================================

def add_programme_tricks_button(request, programme_id):
  #Saved Trick Function - Alter 
  programme = Trick_Programme.objects.get(ProgrammeID=programme_id)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))
  programme.ProgrammeTricks.add(trick)

  messages.info(request, (trick.TrickName + " Has Been Added To The " + programme.ProgrammeName + " Programme!"))
  return HttpResponseRedirect('/add_programme_tricks_list/%d'%programme.ProgrammeID)

# ======================================================================================================================================

def remove_programme_tricks_button(request, programme_id):
  programme = Trick_Programme.objects.get(ProgrammeID=programme_id)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))

  if programme.ProgrammeTricks.filter(TrickID=trick.TrickID).exists():
    programme.ProgrammeTricks.remove(trick)

  messages.error(request, (trick.TrickName + " Has Been Removed From The " + programme.ProgrammeName + " Programme!"))
  return HttpResponseRedirect('/add_programme_tricks_list/%d'%programme.ProgrammeID)

# ======================================================================================================================================

def programme_list(request):

  all_programmes = Trick_Programme.objects.all().order_by('ProgrammeRecLevel', 'ProgrammeDifficulty', 'ProgrammeName')
  programme_count = all_programmes.count()

  #Pagination setup
  p = Paginator(all_programmes, 6)
  page = request.GET.get('page')
  programmes = p.get_page(page)
  num_pages = "T" * programmes.paginator.num_pages

  return render(request, 'main/programme_list.html', {'programmes': programmes, "num_pages":num_pages, "programme_count":programme_count})

# ======================================================================================================================================

def view_programme(request, programme_id):
  Programme = Trick_Programme.objects.get(pk=programme_id)
  Programme_Tricks = Programme.ProgrammeTricks.order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')
  return render(request, 'main/view_programme.html', {'Programme':Programme, 'Programme_Tricks':Programme_Tricks})

# ======================================================================================================================================

def save_programme(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  programme = get_object_or_404(Trick_Programme, ProgrammeID=request.POST.get("programme_id"))
  profile.SavedProgrammes.add(programme)

  messages.info(request, (programme.ProgrammeName + " Has Been Added To Your List Of Saved Programmes!"))
  return HttpResponseRedirect('/home')

# ======================================================================================================================================

def unsave_programme(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  programme = get_object_or_404(Trick_Programme, ProgrammeID=request.POST.get("programme_id"))

  if profile.SavedProgrammes.filter(ProgrammeID=programme.TrickID).exists():
    profile.SavedProgrammes.remove(programme)

  messages.error(request, (programme.ProgrammeName + " Has Been Removed From Your List Of Saved Programmes!"))
  return HttpResponseRedirect('/home')

# ======================================================================================================================================

@permission_required('programme.change_programme', login_url='home')
def update_programme(request, programme_id):
  programme = Trick_Programme.objects.get(pk=programme_id)
  form = ProgrammeForm(request.POST or None, instance=programme)
  if form.is_valid():
    form.save()
    messages.success(request, ("Trick Updated Successfuly!"))
    return HttpResponseRedirect('/programme_list')
  return render(request, 'main/update_programme.html', {'programme':programme, 'form':form})

# ======================================================================================================================================

@permission_required('trick.delete_trick', login_url='home')
def delete_programme(request, programme_id):
  programme = Trick_Programme.objects.get(pk=programme_id)
  programme.delete()
  return HttpResponseRedirect('/programme_list')

# ======================================================================================================================================

@permission_required('category.add_category', login_url='home')
def add_category(request):
    submitted = False
    if request.method == "POST":
      form = CategoryForm(request.POST, request.FILES)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect('/add_category?submitted=True')
    else:
      form = CategoryForm
      if 'submitted' in request.GET:
        submitted = True
        messages.success(request, ("New Category Created!"))
    return render(request, 'main/add_category.html', {'form':form, 'submitted':submitted})

# ======================================================================================================================================

def category_list(request):

  all_categories = Category.objects.all().order_by('CategoryID')

  return render(request, 'main/category_list.html', {'categories': all_categories})

# ======================================================================================================================================

def show_category(request, category_id):

  category = Category.objects.get(pk=category_id)
  category_name = category.CategoryName
  tricks =  Trick.objects.filter(TrickCategory__CategoryName__exact=category_name).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')
  trick_count = tricks.count()
  
  return render(request, 'main/show_category.html', {'category':category, 'tricks':tricks, 'trick_count':trick_count})

# ======================================================================================================================================

@permission_required('category.change_category', login_url='home')
def update_category(request, category_id):
  category = Category.objects.get(pk=category_id)
  form = CategoryForm(request.POST or None, instance=category)
  if form.is_valid():
    form.save()
    messages.success(request, ("Category Updated Successfuly!"))
    return HttpResponseRedirect('/category_list')
  return render(request, 'main/update_category.html', {'category':category, 'form':form})

# ======================================================================================================================================

@permission_required('trick.delete_trick', login_url='home')
def delete_category(request, category_id):
  category = Category.objects.get(pk=category_id)
  category.delete()
  return HttpResponseRedirect('/category_list')

# ======================================================================================================================================


@login_required(login_url='/login')
def admin_db(request):
  # An Extra Level Security for the Admin Panel
  if request.user.is_superuser :
    return HttpResponseRedirect('/admin')
  else:
    return HttpResponseRedirect('/home')

# ======================================================================================================================================

