from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('trick_list', views.trick_list, name="trick-list"),
    path('add_trick', views.add_trick, name='add-trick'),
    path('show_trick/<trick_id>', views.show_trick, name='show-trick'),
    path('update_trick/<trick_id>', views.update_trick, name='update-trick'),
    path('search_trick', views.search_trick, name='search-trick'),
    path('delete_trick/<trick_id>', views.delete_trick, name='delete-trick'),
    path('recommend_trick', views.recommend_trick, name='recommend-trick'),
    path('admin_db', views.admin_db, name='admin-db'),
]
