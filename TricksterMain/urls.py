from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('tricklist', views.all_tricks, name="trick-list"),
]
