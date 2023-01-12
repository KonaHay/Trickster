from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# Imports for Pagination
from django.core.paginator import Paginator

#--- for if using MongoDB database ---
#import pymongo
#from pymongo import MongoClient

from .models import Trick
from .forms import TrickForm


def home(request):
  return render(request, 'main/home.html', {})

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

def trick_list(request):
  #------ For view based paginator ---------
  #num_pages = t_paginator.paginator_pages
  #tricks = t_paginator.paginator_tricks
  #-----------------------------------------

  #Pagination setup
  all_tricks = Trick.objects.all().order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')
  p = Paginator(all_tricks, 6)
  page = request.GET.get('page')
  tricks = p.get_page(page)
  num_pages = "T" * tricks.paginator.num_pages

  return render(request, 'main/trick_list.html', {'tricks': tricks, "num_pages":num_pages})

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
    return render(request, 'main/add_trick.html', {'form' : form, 'submitted':submitted})

def show_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  return render(request, 'main/show_trick.html', {'trick' : trick})

@permission_required('trick.change_trick', login_url='home')
def update_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  form = TrickForm(request.POST or None, instance=trick)
  if form.is_valid():
    form.save()
    messages.success(request, ("Trick Updated Successfuly!"))
    return HttpResponseRedirect('/trick_list')
  return render(request, 'main/update_trick.html', {'trick':trick, 'form':form})

def search_trick(request):
  if request.method == "POST":
    trick_searched = request.POST['trick_searched']
    tricks =  Trick.objects.filter(TrickName__contains=trick_searched).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

    return render(request, 'main/search_trick.html', {'trick_searched':trick_searched, 'tricks':tricks})
  else:
    return render(request, 'main/search_trick.html', {})

@permission_required('trick.delete_trick', login_url='home')
def delete_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  trick.delete()
  return HttpResponseRedirect('/trick_list')

@login_required(login_url='/login')
def admin_db(request):
  # An Extra Level Security for the Admin Panel
  if request.user.is_superuser :
    return HttpResponseRedirect('/admin')
  else:
    return HttpResponseRedirect('/home')


# --- For connecting to MongoDB Database ---
# client = pymongo.MongoClient('mongodb+srv://admin:admin@trickster.v1hgxhs.mongodb.net/?retryWrites=true&w=majority')

# #Define the DB Name
# dbname = client['TricksterDB']

# #Define the Collection
# cl = dbname['Trickster']

# #Testing
# trickster_test={
#     "name":"Kona",
#     "age":"22",
#     "skillLevel":"2"
# }

# cl.insert_one(trickster_test)

# Trickster_Details = cl.find({})