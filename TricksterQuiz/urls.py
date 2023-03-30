from django.urls import path
from . import views

urlpatterns = [
    
  # -- Pages -- 
  path('skill_level_quiz', views.skill_level_quiz, name='skill-level-quiz'),
  path('quiz_underway/<int:pk>', views.quiz_underway, name='quiz-underway'),
  path('quiz_results/<int:pk>', views.quiz_results, name='quiz-results'),

  # -- Components --
  path('quiz_underway/<int:pk>/data/', views.quiz_data, name='quiz-data'),
  path('quiz_underway/<int:pk>/tricks/', views.quiz_tricks, name='quiz-tricks'),
  path('quiz_underway/<int:pk>/next/', views.next_quiz, name='next-quiz'),
  path('quiz_underway/<int:pk>/save/', views.save_quiz, name='save-quiz'),
  path('quiz_trick_card', views.quiz_trick_card, name='quiz-trick-card'),
  path('quiz_learned_trick_button/<int:pk>', views.quiz_learned_trick_button, name='quiz-learned-trick-button'),

]