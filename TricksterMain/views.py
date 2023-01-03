import pymongo
from django.shortcuts import render
#from pymongo import MongoClient
from django.http import HttpResponseRedirect

from .models import Trick
from .forms import TrickForm


def home(request):
    return render(request, 'main/home.html', {})

def all_tricks(request):
    trick_list = Trick.objects.all()
    return render(request, 'main/trick_list.html', {'trick_list': trick_list})

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


# #Connecting to Tricksters MongoDB Database
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