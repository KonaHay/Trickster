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
    path('recommend_trick/<int:pk>', views.recommend_trick, name='recommend-trick'),
    path('learned_trick/<int:pk>', views.learned_trick, name='learned-trick'),
    path('unlearn_trick/<int:pk>', views.unlearn_trick, name='unlearn-trick'),
    path('save_trick/<int:pk>', views.save_trick, name='save-trick'),
    path('unsave_trick/<int:pk>', views.unsave_trick, name='unsave-trick'),
    path('random_trick', views.random_trick, name='random-trick'),
    path('random_trick_skill_based/<int:pk>', views.random_trick_skill_based, name='random-trick-skill-based'),
    path('random_trick_learned/<int:pk>', views.random_trick_learned, name='random-trick-learned'),
    path('trick_card', views.trick_card, name='trick-card'),
    path('add_category', views.add_category, name='add-category'),
    path('category_list', views.category_list, name="category-list"),
    path('show_category/<category_id>', views.show_category, name='show-category'),
    path('update_category/<category_id>', views.update_category, name='update-category'),
    path('delete_category/<category_id>', views.delete_category, name='delete-category'),

    #Skill Programme URL's
    path('add_programme', views.add_programme, name='add-programme'),
    path('add_programme_success/<programme_id>', views.add_programme_success, name='add-programme-success'),
    path('add_programme_tricks_list/<programme_id>', views.add_programme_tricks_list, name='add-programme-tricks-list'),
    path('add_programme_tricks_button/<programme_id>', views.add_programme_tricks_button, name='add-programme-tricks-button'),
    path('remove_programme_tricks_button/<programme_id>', views.remove_programme_tricks_button, name='remove-programme-tricks-button'),
    path('programme_list', views.programme_list, name="programme-list"),
    path('view_programme/<programme_id>', views.view_programme, name='view-programme'),
    path('unsave_programme/<int:pk>', views.unsave_programme, name='unsave-programme'),
    path('save_programme/<int:pk>', views.save_programme, name='save-programme'),
    path('update_programme/<programme_id>', views.update_programme, name='update-programme'),
    path('delete_programme/<programme_id>', views.delete_programme, name='delete-programme'),

    #Admin URL's
    path('admin_db', views.admin_db, name='admin-db'),
]
