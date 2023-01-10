from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

# Imports for Pagination
from django.core.paginator import Paginator

#--- for if using MongoDB database ---
#import pymongo
#from pymongo import MongoClient

from .models import Trick
from .forms import TrickForm


def home(request):
  return render(request, 'main/home.html', {})

def all_tricks(request):
  tricks = Trick.objects.all().order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

  #Pagination setup
  p = Paginator(tricks, 6)
  page = request.GET.get('page')
  trick_list = p.get_page(page)
  num_pages = "T" * trick_list.paginator.num_pages

  return render(request, 'main/trick_list.html', {'trick_list': trick_list, "num_pages":num_pages})

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

def delete_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  trick.delete()
  return HttpResponseRedirect('/trick_list')




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