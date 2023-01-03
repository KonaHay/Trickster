from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('trick_list', views.all_tricks, name="trick-list"),
    path('add_trick', views.add_trick, name='add-trick'),
]
