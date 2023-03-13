from django.urls import path
from . import views

urlpatterns = [
    path('skill_level_quiz', views.skill_level_quiz, name='skill-level-quiz'),
]