from django.urls import path
from . import views

urlpatterns = [
    path('user_login', views.user_login, name='login'),
    path('user_logout', views.user_logout, name='logout'),
    path('register_user', views.register_user, name='register_user'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('following/<int:pk>', views.following, name='following'),
    path('followers/<int:pk>', views.followers, name='followers'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('my_skill_level/<int:pk>', views.my_skill_level, name='my-skill-level'),
    path('my_tricks/<int:pk>', views.my_tricks, name="my-tricks"),
    path('my_completed_programmes/<int:pk>', views.my_completed_programmes, name="my-completed-programmes"),
    path('my_saved_tricks/<int:pk>', views.my_saved_tricks, name="my-saved-tricks"),
    path('my_saved_programmes/<int:pk>', views.my_saved_programmes, name="my-saved-programmes"),
    path('update_profile/<int:pk>', views.update_profile, name='update-profile'),
]