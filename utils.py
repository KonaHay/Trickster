from django.urls import path
from pymongo import MongoClient

def get_db_handle():
    client = MongoClient("mongodb+srv://admin:admin@trickster.v1hgxhs.mongodb.net/?retryWrites=true&w=majority")
    db = client['TricksterDB']
    
    return client


client = get_db_handle()

db = client.get_database("TricksterDB")

cl = db.get_collection("Trickster")
print(cl.find_one({"idtest":1}))