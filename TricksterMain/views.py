import pymongo
from django.shortcuts import render
from pymongo import MongoClient

def home(request):
    return render(request, 'home.html', {})



#Connecting to Tricksters MongoDB Database
client = pymongo.MongoClient('mongodb+srv://admin:admin@trickster.v1hgxhs.mongodb.net/?retryWrites=true&w=majority')

#Define the DB Name
dbname = client['TricksterDB']

#Define the Collection
cl = dbname['Trickster']

#Testing
trickster_test={
    "name":"Kona",
    "age":"22",
    "skillLevel":"2"
}

cl.insert_one(trickster_test)

Trickster_Details = cl.find({})