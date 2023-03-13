from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from .models import  Skill_Level_Quiz
#from .forms import 
#from TricksterMain.models import Trick, SkillLevel

def skill_level_quiz(request):

    return render(request, 'skill_level_quiz.html')
