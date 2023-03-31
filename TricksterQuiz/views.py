from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
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
  quiz = Skill_Level_Quiz.objects.get(QuizID=quizSection.SectionQuiz.QuizID)
  section_tricks = Section_Trick.objects.filter(TrickSection=quizSection).order_by('TrickValue')

  current_page = request.path
  return render(request, 'pages/quiz_underway.html', {'quiz':quiz, 'quizSection':quizSection, 'section_tricks':section_tricks, 'current_page':current_page})

# ======================================================================================================================================

# -- Components -- 

def quiz_data(request, pk):
  quizSection = Quiz_Section.objects.get(SectionNumber=pk)
  quiz = Skill_Level_Quiz.objects.get(QuizID=quizSection.SectionQuiz.QuizID)
  term_bonus = Term_Bonus.objects.get(BonusSection=quizSection.SectionID)

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
  quizSection = Quiz_Section.objects.get(SectionNumber=pk)
  quiz = Skill_Level_Quiz.objects.get(QuizID=quizSection.SectionQuiz.QuizID)
  section_tricks = Section_Trick.objects.filter(TrickSection=quizSection.SectionID).order_by('TrickValue')

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
    trickScore = data_.get("score")
    trickScore = int(trickScore[0])
    data_.pop("score")

    for key in data_.keys():
      # Need to pass the TermID not the KeyWord!
      Term = Glossary_Term.objects.get(KeyWord=key)
      question = Bonus_Question.objects.get(QuestionTerm=Term)
      questions.append(question)

    user = request.user
    profile = User_Profile.objects.get(User_id=user.UserID)
    bonusQuiz = Term_Bonus.objects.get(pk=pk)
    section = bonusQuiz.BonusSection

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

    Section_Result.objects.create(ResultSection=section, ResultBonus=bonusQuiz, ResultUser=profile, TrickScore=trickScore, BonusScore=bonusScore)
    
    sectionID = section.SectionID
    failScore = section.SectionFailScore
    passScore = section.SectionPassScore
    nextSectionID = 0

    finalSection=False
    failedSection=False

    if trickScore >= passScore:
      nextSectionID = sectionID+1
      thisSectionID = sectionID
      if nextSectionID > 4:
        finalSection=True
        nextSectionID=5
    elif trickScore <= failScore:
      failedSection=True
      previousSectionID = sectionID-1
      nextSectionID=5
    else:
      finalSection=True
      thisSectionID = sectionID
      nextSectionID=5

    if finalSection:
      skillLevel, masteryLevel = calculate_skill_level(profile, thisSectionID)
      
      profile.MasteryLevel = masteryLevel
      profile.SkillLevel = skillLevel
      profile.LevelProgress = 10
      profile.completed_skill_quiz=True
      profile.save()
      Section_Result.objects.filter(ResultUser=profile).delete()

    elif failedSection:
      # Take results from last section and assign skill level)
      skillLevel, masteryLevel = calculate_skill_level(profile, previousSectionID)
      
      profile.MasteryLevel = masteryLevel
      profile.SkillLevel = skillLevel
      profile.LevelProgress = 10
      profile.completed_skill_quiz=True
      profile.save()
      Section_Result.objects.filter(ResultUser=profile).delete()

  
  return JsonResponse({'score': trickScore, 'nextSection': nextSectionID})

# ======================================================================================================================================

def calculate_skill_level(profile, sectionID):
  sectionResults = Section_Result.objects.get(ResultUser=profile, ResultSection=sectionID)
  quizSection = Quiz_Section.objects.get(pk=sectionID)
  sectionScore = sectionResults.TrickScore
  sectionBonus = sectionResults.BonusScore
  skillLevel = quizSection.SectionLevel
  masteryLevel = 0

  #Score to Mastery Level Conversion
  if sectionScore <= 5:
    masteryLevel=1
  elif sectionScore <= 11:
    masteryLevel=3
  elif sectionScore <= 23:
    masteryLevel=5
  elif sectionScore <= 35:
    masteryLevel=6
  elif sectionScore <= 47:
    masteryLevel=7
  elif sectionScore <= 63:
    masteryLevel=8
  
  #Bonus Conversion
  if sectionBonus == 3:
    masteryLevel = masteryLevel +2
  elif sectionBonus == 2:
    masteryLevel = masteryLevel +1
    
  return skillLevel, masteryLevel

# ======================================================================================================================================

def quiz_trick_card(request, pk):

  return render(request, 'components/quiz_trick_cards.html', {})

# ======================================================================================================================================

def quiz_results(request, pk):

  if request.user.is_authenticated:
    profile = User_Profile.objects.get(User_id=pk)
    user = Trickster_User.objects.get(UserID=pk)

    skillLevel = profile.SkillLevel
    masteryLevel = profile.MasteryLevel

    return render(request, 'pages/quiz_results.html', {'profile':profile, 'skillLevel':skillLevel, 'masteryLevel':masteryLevel})

  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return redirect('home')


# ======================================================================================================================================


