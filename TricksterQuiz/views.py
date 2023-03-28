from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView

from .models import  Skill_Level_Quiz, Quiz_Section, Section_Trick, Term_Bonus, Bonus_Question, Bonus_Answer, Section_Result
from TricksterMain.models import Trick, SkillLevel, Glossary_Term
from Users.models import Trickster_User, User_Profile



# Function for detexting ajax calls.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# ======================================================================================================================================

def skill_level_quiz(request):
  Skill_Quiz = Skill_Level_Quiz.objects.get(QuizID=1)

  return render(request, 'pages/skill_level_quiz.html', {'Skill_Quiz':Skill_Quiz})

# ======================================================================================================================================

def quiz_underway(request, pk):
  quizSection = Quiz_Section.objects.get(SectionNumber=pk)
  quiz = Skill_Level_Quiz.objects.filter(QuizID=quizSection.SectionQuiz.QuizID)
  section_tricks = Section_Trick.objects.filter(TrickSection=quizSection).order_by('TrickValue')

  current_page = request.path
  return render(request, 'pages/quiz_underway.html', {'quiz':quiz, 'quizSection':quizSection, 'section_tricks':section_tricks, 'current_page':current_page})

# ======================================================================================================================================

# -- Components -- 

def quiz_data(request, pk):
  quiz = Skill_Level_Quiz.objects.get(QuizID=pk)
  quiz_section = Quiz_Section.objects.get(SectionQuiz=quiz.QuizID)
  term_bonus = Term_Bonus.objects.get(BonusSection=quiz_section.SectionID)

  questions = []
  for q in term_bonus.get_questions():
    answers=[]
    for a in q.get_answers():
      answers.append(a.AnswerText)
    questions.append({str(q.QuestionTerm): answers})

  return JsonResponse({
    'data': questions,
  })

# ======================================================================================================================================

def quiz_tricks(request, pk):
  quiz = Skill_Level_Quiz.objects.get(QuizID=pk)
  quiz_section = Quiz_Section.objects.get(SectionQuiz=quiz.QuizID)
  section_tricks = Section_Trick.objects.filter(TrickSection=quiz_section.SectionID).order_by('TrickValue')

  tricks = []
  for trick in section_tricks:
    img = trick.Trick.TrickImg
    value = trick.TrickValue
    tricks.append({str(trick.Trick): value})

  return JsonResponse({
    'data': tricks,
  })

# ======================================================================================================================================

def next_quiz(request, pk):
  #print(request.POST)
  if is_ajax(request=request):
    tricks= []
    data = request.POST
    data_ = dict(data.lists())
    data_.pop('csrfmiddlewaretoken')

    user = request.user
    profile = User_Profile.objects.get(User_id=user.UserID)
    quiz = Term_Bonus.objects.get(pk=pk)
    section = quiz.BonusSection

    trickScore = 0
    results = []

    for key in data_.keys():
      trick = Trick.objects.get(TrickName=key)
      selectedTrick = Section_Trick.objects.get(Trick=trick.TrickID)

      trickName = trick.TrickName
      trickValue = selectedTrick.TrickValue

      #profile.LearnedTricks.add(trick)
      trickScore += trickValue

      results.append({str(trickName): {'Trick': trickName, 'score': trickValue}})
      tricks.append(trick)

  return JsonResponse({'score': trickScore, 'results': results})

# ======================================================================================================================================

def quiz_bonus(request, pk):
  quiz = Skill_Level_Quiz.objects.get(QuizID=pk)

  current_page = request.path
  return render(request, 'pages/quiz_bonus.html', {'quiz':quiz, 'current_page':current_page})

  return 

# ======================================================================================================================================

def save_quiz(request, pk):
  #print(request.POST)
  if is_ajax(request=request):

    questions= []
    data = request.POST
    data_ = dict(data.lists())

    data_.pop('csrfmiddlewaretoken')
    messages.error(request, (data_))
    trickScore = data_.get("score")
    data_.pop("score")

    for key in data_.keys():
      # Need to pass the TermID not the KeyWord!
      Term = Glossary_Term.objects.get(KeyWord=key)
      question = Bonus_Question.objects.get(QuestionTerm=Term)
      questions.append(question)

    user = request.user
    profile = User_Profile.objects.get(User_id=user.UserID)
    quiz = Term_Bonus.objects.get(pk=pk)
    section = quiz.BonusSection

    bonusScore = 0
    results = []
    correct_answer = None

    for q in questions:
      ans_selected = request.POST.get(str(q.QuestionTerm))

      if ans_selected != "":
        question_answers = Bonus_Answer.objects.filter(AnswerQuestion=q)
        for ans in question_answers:
          if ans_selected == ans.AnswerText:
            if ans.AnswerCorrect:
              bonusScore += 1
              correct_answer = ans.AnswerText
          else:
            if ans.AnswerCorrect:
              correct_answer = ans.AnswerText
        
        results.append({str(q.QuestionTerm): {'correct_answer': correct_answer, 'answered': ans_selected}})
      else:
        results.append({str(q.QuestionTerm): 'not answered'})

    Section_Result.objects.create(ResultSection=section, ResultBonus=quiz, ResultUser=profile, TrickScore=trickScore, BonusScore=bonusScore)
  
    section = section.SectionID
    nextSection = section+1
  return HttpResponseRedirect('quiz_underway/%d'%nextSection)()

# ======================================================================================================================================

def quiz_trick_card(request, pk):

  return render(request, 'components/quiz_trick_cards.html', {})

# ======================================================================================================================================

def quiz_learned_trick_button(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))
  profile.LearnedTricks.add(trick)

  current_page = request.POST.get("current_page")
  messages.info(request, (trick.TrickName + " Has Been Added To Your List Of Learned Tricks!"))
  return redirect(current_page)

# ======================================================================================================================================

def quiz_unlearn_trick_button(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))

  if profile.LearnedTricks.filter(TrickID=trick.TrickID).exists():
    profile.LearnedTricks.remove(trick)

  current_page = request.POST.get("current_page")
  messages.error(request, (trick.TrickName + " Has Been Removed From Your List Of Learned Tricks!"))
  return redirect(current_page)

# ======================================================================================================================================


