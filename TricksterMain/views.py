from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator

from random import shuffle

from .models import Trick, SkillLevel, Trick_Programme, Category, Programme_Lesson, Glossary_Term
from .forms import TrickForm, ProgrammeForm, CategoryForm, LessonForm, GlossaryTermForm, SubmitTrickForm
from Users.models import Trickster_User, User_Profile 


def carousel_test(request):
  return render(request, 'main/carousel_test.html', {})

def home(request):
  beginners_guide = Trick_Programme.objects.get(ProgrammeID=1)
  how_to_ollie = Trick.objects.get(TrickID=15)

  return render(request, 'main/home.html', {'beginners_guide':beginners_guide, 'how_to_ollie':how_to_ollie})

# ======================================================================================================================================

def trick_list(request):

  all_tricks = Trick.objects.filter(approved=True).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')
  trick_count = all_tricks.count()

  #Pagination setup
  p = Paginator(all_tricks, 12)
  page = request.GET.get('page')
  tricks = p.get_page(page)
  num_pages = "T" * tricks.paginator.num_pages

  current_page = request.path
  if page:
    current_page = current_page + "?page=" + page

  return render(request, 'main/trick_list.html', {'tricks': tricks, "num_pages":num_pages, "trick_count":trick_count, "current_page":current_page})

# ======================================================================================================================================

# View for recommending tricks to users
def recommend_trick(request, pk):
  if request.user.is_authenticated:
    current_page = request.path

    profile = User_Profile.objects.get(User_id=pk)
    user_learned_tricks = profile.LearnedTricks
    user_skill_level = profile.SkillLevel
    user_ability = profile.MasteryLevel

    learned_tricks = user_learned_tricks.order_by('TrickName')
    user_learned_trick_names = learned_tricks

    filters = models.Q()

    #Trying to filter by if the user has NOT learned the trick (~models.Q used to get Non Learned Tricks)
    #if user_learned_tricks: .exclude(TrickName__LearnedTricks=user_learned_trick_names)
    #filters &= ~models.Q(Trick__LearnedTricks=user_learned_tricks,)

    filters &= models.Q(TrickRecLevel=user_skill_level) & models.Q(TrickDifficulty=user_ability)

    recommend_tricks = Trick.objects.filter(filters).order_by('TrickName')
    messages.error(request, (learned_tricks))

    #Try to use paginator to put tricks into a carosel.


    return render(request, 'main/recommend_trick.html', {'recommend_tricks': recommend_tricks, 'profile': profile, 'user_learned_tricks':user_learned_tricks, 'current_page':current_page})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return HttpResponseRedirect('/home')

# ======================================================================================================================================

def random_trick(request):
  if request.method == "POST":
    current_page = request.path

    random_trick = Trick.objects.filter(approved=True).order_by('?').first()

    return render(request, 'main/random_trick.html', {'random_trick':random_trick, 'current_page':current_page})
  else:
    return render(request, 'main/random_trick.html', {})

# ======================================================================================================================================

def random_trick_skill_based(request, pk):
  if request.user.is_authenticated:
    if request.method == "POST":
      current_page = request.path

      profile = User_Profile.objects.get(User_id=pk)
      user_skill_level = profile.SkillLevel
      user_ability = profile.UserDifficultyLevel

      filters = models.Q()

      filters &= models.Q(TrickRecLevel=user_skill_level) & models.Q(TrickDifficulty=user_ability)

      filters &= models.Q(approved=True)

      random_trick = Trick.objects.filter(filters).order_by('?').first()

      return render(request, 'main/random_trick_skill_based.html', {'random_trick': random_trick, 'profile': profile, 'current_page':current_page})
    else:
      return render(request, 'main/random_trick_skill_based.html', {})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return HttpResponseRedirect('/home')

# ======================================================================================================================================

def random_trick_learned(request, pk):
  if request.user.is_authenticated:
    if request.method == "POST":
      current_page = request.path

      profile = User_Profile.objects.get(User_id=pk)
      user_learned_tricks = profile.LearnedTricks

      random_trick = user_learned_tricks.order_by('?').first()
      
      return render(request, 'main/random_trick_learned.html', {'random_trick': random_trick, 'profile': profile, 'current_page':current_page})
    else:
      return render(request, 'main/random_trick_learned.html', {})
  else:
    messages.error(request, ("You Must Be Logged In To See This Page!"))
    return HttpResponseRedirect('/home')

# ======================================================================================================================================

def learned_trick(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))
  profile.LearnedTricks.add(trick)
  progressIncrease, levelUpMessage = progress_increase(profile.pk, 5)
  if progressIncrease==False:
    messages.success(request, (levelUpMessage))

  current_page = request.POST.get("current_page")
  messages.info(request, (trick.TrickName + " Has Been Added To Your List Of Learned Tricks!"))
  return redirect(current_page)

# ======================================================================================================================================

def unlearn_trick(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))
  trickXP = 5

  if profile.LearnedTricks.filter(TrickID=trick.TrickID).exists():
    profile.LearnedTricks.remove(trick)
    progressDecrease, levelDownMessage = progress_decrease(profile.pk, 5)
    if progressDecrease==False:
      messages.error(request, (levelDownMessage))
    

  current_page = request.POST.get("current_page")
  messages.error(request, (trick.TrickName + " Has Been Removed From Your List Of Learned Tricks!"))
  return redirect(current_page)

# ======================================================================================================================================

def progress_increase(profileID, percentageIncrease):
  profile = User_Profile.objects.get(pk=profileID)

  progressIncrease=False
  masteryLevelUp=False
  skillLevelUp=False
  maxLevel=False
  levelUpMessage = ""

  currentSkillLevelID = profile.SkillLevel.SkillLevelID
  currentMasteryLevel = profile.MasteryLevel
  currentProgress = profile.LevelProgress

  newProgressAmount = currentProgress + percentageIncrease
  progressIncrease=True
  if newProgressAmount >= 100:
    masteryLevelUp=True
    newProgressAmount = newProgressAmount-100
    newMasteryLevel = currentMasteryLevel+1
    if newMasteryLevel >= 11:
      newMasteryLevel = newMasteryLevel-10
      newSkillLevelID = currentSkillLevelID+1
      if newSkillLevelID >= 8:
        maxLevel=True
      else:
        skillLevelUp=True
        newSkillLevel = SkillLevel.objects.get(SkillLevelID=newSkillLevelID)

  profile.LevelProgress = newProgressAmount
  if masteryLevelUp:
    progressIncrease=False
    levelUpMessage = "Congradulations, you have leveled up to Mastery Level "+ str(newMasteryLevel)+"!"
    profile.MasteryLevel = newMasteryLevel
    if skillLevelUp:
      levelUpMessage = "Congradulations, your Skill Level has leveld up to "+newSkillLevel.SkillLevelName+"!"
      profile.SkillLevel = newSkillLevel
      if maxLevel:
        levelUpMessage = "Wow! You have reached the Max Level on Trickster!"

  profile.save()
    
  return progressIncrease, levelUpMessage

# ======================================================================================================================================

def progress_decrease(profileID, percentageDecrease):
  profile = User_Profile.objects.get(pk=profileID)

  progressDecrease=False
  masteryLevelDown=False
  skillLevelDown=False
  lowestLevel=False
  leveldownMessage = ""

  currentSkillLevelID = profile.SkillLevel.SkillLevelID
  currentMasteryLevel = profile.MasteryLevel
  currentProgress = profile.LevelProgress

  newProgressAmount = currentProgress - percentageDecrease
  progressDecrease=True
  if newProgressAmount < 0:
    masteryLevelDown=True
    newProgressAmount = newProgressAmount+100
    newMasteryLevel = currentMasteryLevel-1
    if newMasteryLevel <= 0:
      newMasteryLevel = newMasteryLevel+10
      newSkillLevelID = currentSkillLevelID-1
      if newSkillLevelID <= 4:
        lowestLevel=True
        masteryLevelDown=False
        skillLevelDown=False
        newProgressAmount=0
      else:
        skillLevelDown=True
        newSkillLevel = SkillLevel.objects.get(SkillLevelID=newSkillLevelID)

  profile.LevelProgress = newProgressAmount
  if masteryLevelDown:
    progressDecrease=False
    leveldownMessage = "Unfortunate, your Mastery Level has been dropped to "+ str(newMasteryLevel)+"!"
    profile.MasteryLevel = newMasteryLevel
    if skillLevelDown:
      leveldownMessage = "Unfortunate, your Skill Level has been dropped to "+newSkillLevel.SkillLevelName+"!"
      profile.SkillLevel = newSkillLevel
      if lowestLevel:
        progressDecrease=True


  profile.save()
    
  return progressDecrease, leveldownMessage

# ======================================================================================================================================

def save_trick(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))
  profile.SavedTricks.add(trick)

  current_page = request.POST.get("current_page")
  messages.info(request, (trick.TrickName + " Has Been Added To Your List Of Saved Tricks!"))
  return redirect(current_page)

# ======================================================================================================================================

def unsave_trick(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))

  if profile.SavedTricks.filter(TrickID=trick.TrickID).exists():
    profile.SavedTricks.remove(trick)

  current_page = request.POST.get("current_page")
  messages.error(request, (trick.TrickName + " Has Been Removed From Your List Of Saved Tricks!"))
  return redirect(current_page)

# ======================================================================================================================================

@permission_required('trick.add_trick', login_url='home')
def add_trick(request):
    submitted = False
    if request.method == "POST":
      form = TrickForm(request.POST, request.FILES)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect('/add_trick?submitted=True')
    else:
      form = TrickForm
      if 'submitted' in request.GET:
        submitted = True
        messages.success(request, ("Trick Added Successfuly!"))
    return render(request, 'main/add_trick.html', {'form':form, 'submitted':submitted})

# ======================================================================================================================================

def show_trick(request, trick_id):
  current_page = request.path

  trick = Trick.objects.get(pk=trick_id)
  return render(request, 'main/show_trick.html', {'trick':trick, 'current_page':current_page})

# ======================================================================================================================================

@permission_required('trick.change_trick', login_url='home')
def update_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  form = TrickForm(request.POST or None, request.FILES or None, instance=trick)
  if form.is_valid():
    form.save()
    messages.success(request, ("Trick Updated Successfuly!"))
    return HttpResponseRedirect('/trick_list')
  return render(request, 'main/update_trick.html', {'trick':trick, 'form':form})

# ======================================================================================================================================

def submit_trick(request):
    submitted = False
    if request.method == "POST":
      form = SubmitTrickForm(request.POST, request.FILES)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect('/submit_trick?submitted=True')
    else:
      form = SubmitTrickForm
      if 'submitted' in request.GET:
        submitted = True
        messages.success(request, ("Trick Submitted Successfuly!"))
    return render(request, 'main/submit_trick.html', {'form':form, 'submitted':submitted})

# ======================================================================================================================================

@permission_required('trick.change_trick', login_url='home')
def approve_tricks(request):

  unapproved_tricks = Trick.objects.filter(approved=False).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')
  trick_count = unapproved_tricks.count()

  return render(request, 'main/approve_tricks.html', {'unapproved_tricks': unapproved_tricks, "trick_count":trick_count})

# ======================================================================================================================================

#The 'current_page' redirect method doesnt work right with search as it does not maintain the searched value
def search_trick(request):
  if request.method == "POST":
    current_page = request.path

    trick_searched = request.POST['trick_searched']
    tricks = Trick.objects.filter(approved=True, TrickName__contains=trick_searched).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

    return render(request, 'main/search_trick.html', {'trick_searched':trick_searched, 'tricks':tricks, 'current_page':current_page})
  else:
    return render(request, 'main/search_trick.html', {})

# ======================================================================================================================================

@permission_required('trick.delete_trick', login_url='home')
def delete_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  trick.delete()
  messages.error(request, ("Trick '" + trick.TrickName + "' has been Deleted!"))
  return HttpResponseRedirect('/trick_list')

# ======================================================================================================================================

@permission_required('trick.delete_trick', login_url='home')
def delete_unapproved_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  trick.delete()
  messages.error(request, ("Trick '" + trick.TrickName + "' has been Deleted!"))
  return HttpResponseRedirect('/approve_tricks')

# ======================================================================================================================================

@permission_required('trick.change_trick', login_url='home')
def approve_trick(request, trick_id):
  trick = Trick.objects.get(pk=trick_id)
  Trick.objects.filter(pk=trick.TrickID).update(approved=True)
  messages.success(request, ("Trick '" + trick.TrickName + "' has been Approved!"))
  return HttpResponseRedirect('/approve_tricks')

# ======================================================================================================================================

def trick_card(request, pk):

  return render(request, 'components/trick_cards.html', {})

# ======================================================================================================================================

@permission_required('trick.add_programme', login_url='home')
def add_programme(request):
  submitted = False
  if request.method == "POST":
    form = ProgrammeForm(request.POST, request.FILES)
    if form.is_valid():
      new_programme = form.save()
      #need to pass the ProgrammeID after its been created.
      programme = new_programme
      return HttpResponseRedirect('/add_programme_success/%d'%programme.ProgrammeID)
  else:
    form = ProgrammeForm
    if 'submitted' in request.GET:
      submitted = True
      messages.success(request, ("Trick Programme Added Successfully!"))
  return render(request, 'main/add_programme.html', {'form':form, 'submitted':submitted})

# ======================================================================================================================================

def add_programme_success(request, programme_id):
  Programme = Trick_Programme.objects.get(pk=programme_id)

  return render(request, 'main/add_programme_success.html', {'Programme':Programme})

# ======================================================================================================================================

@permission_required('trick.add_programme', login_url='home')
def add_programme_lessons(request, programme_id):

  Programme = Trick_Programme.objects.get(pk=programme_id)

  submitted = False
  if request.method == "POST":
    form = LessonForm(request.POST, request.FILES)
    if form.is_valid():
      form.instance.Programme = Programme
      form.save()
      messages.success(request, ("Lesson Added Successfully!"))
      return HttpResponseRedirect('/add_programme_success/%d'%Programme.ProgrammeID)
  else:
    form = LessonForm
    if 'submitted' in request.GET:
      submitted = True
      messages.success(request, ("Lesson Added Successfully!"))
  return render(request, 'main/add_programme_lessons.html', {'Programme':Programme, 'form':form, 'submitted':submitted})

# ======================================================================================================================================

@permission_required('trick.add_programme', login_url='home')
def add_programme_tricks_list(request, programme_id):

  all_tricks = Trick.objects.filter(approved=True).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

  Programme = Trick_Programme.objects.get(pk=programme_id)
  Programme_Tricks = Programme.ProgrammeTricks.order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

  #Search Trick Function
  if request.method == "POST":
    trick_searched = request.POST['trick_searched']
    searched_tricks =  Trick.objects.filter(TrickName__contains=trick_searched).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

    return render(request, 'main/add_programme_tricks.html', {
      'Programme':Programme, 
      'Programme_Tricks':Programme_Tricks, 
      'all_tricks':all_tricks, 
      'trick_searched':trick_searched, 
      'searched_tricks':searched_tricks
      })
  else:
    return render(request, 'main/add_programme_tricks.html', {
    'Programme':Programme, 
    'Programme_Tricks':Programme_Tricks, 
    'all_tricks':all_tricks, 
    })

# ======================================================================================================================================

def add_programme_tricks_button(request, programme_id):
  #Saved Trick Function - Alter 
  programme = Trick_Programme.objects.get(ProgrammeID=programme_id)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))
  programme.ProgrammeTricks.add(trick)

  messages.info(request, (trick.TrickName + " Has Been Added To The " + programme.ProgrammeName + " Programme!"))
  return HttpResponseRedirect('/add_programme_tricks_list/%d'%programme.ProgrammeID)

# ======================================================================================================================================

def remove_programme_tricks_button(request, programme_id):
  programme = Trick_Programme.objects.get(ProgrammeID=programme_id)
  trick = get_object_or_404(Trick, TrickID=request.POST.get("trick_id"))

  if programme.ProgrammeTricks.filter(TrickID=trick.TrickID).exists():
    programme.ProgrammeTricks.remove(trick)

  messages.error(request, (trick.TrickName + " Has Been Removed From The " + programme.ProgrammeName + " Programme!"))
  return HttpResponseRedirect('/add_programme_tricks_list/%d'%programme.ProgrammeID)

# ======================================================================================================================================

def programme_list(request):

  all_programmes = Trick_Programme.objects.all().order_by('ProgrammeRecLevel', 'ProgrammeDifficulty', 'ProgrammeName')
  programme_count = all_programmes.count()

  #Pagination setup
  p = Paginator(all_programmes, 6)
  page = request.GET.get('page')
  programmes = p.get_page(page)
  num_pages = "T" * programmes.paginator.num_pages

  return render(request, 'main/programme_list.html', {'programmes': programmes, "num_pages":num_pages, "programme_count":programme_count})

# ======================================================================================================================================

def view_programme(request, programme_id):
  current_page = request.path

  Programme = Trick_Programme.objects.get(pk=programme_id)
  Programme_Tricks = Programme.ProgrammeTricks.order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')

  Lessons = Programme_Lesson.objects.filter(Programme=programme_id).order_by('LessonNumber')
  return render(request, 'main/view_programme.html', {'Programme':Programme, 'Programme_Tricks':Programme_Tricks, 'Lessons':Lessons, 'current_page':current_page})

# ======================================================================================================================================

def learned_lesson(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  lesson = get_object_or_404(Programme_Lesson, LessonID=request.POST.get("lesson_id"))
  profile.CompletedLessons.add(lesson)
  progressIncrease, levelUpMessage = progress_increase(profile.pk, 10)
  if progressIncrease==False:
    messages.success(request, (levelUpMessage))

  programme = lesson.Programme
  programme_lessons = Programme_Lesson.objects.filter(Programme=programme.ProgrammeID).order_by('LessonNumber')

  programme_lessons_learned = profile.CompletedLessons.filter(Programme=programme.ProgrammeID)

  if list(programme_lessons) == list(programme_lessons_learned):
    profile.CompletedProgrammes.add(programme)
    messages.success(request, ("Congradulations! You Have Completed The " + programme.ProgrammeName + " Programme!"))
    progressIncrease, levelUpMessage = progress_increase(profile.pk, 15)
    if progressIncrease==False:
      messages.success(request, (levelUpMessage))

  messages.success(request, (lesson.LessonName + " Has Been Marked As Learned!"))
  return HttpResponseRedirect('/view_programme/%d'%programme.ProgrammeID)
  # get to return to the same page

# ======================================================================================================================================

def unlearn_lesson(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  lesson = get_object_or_404(Programme_Lesson, LessonID=request.POST.get("lesson_id"))

  programme = lesson.Programme

  if profile.CompletedLessons.filter(LessonID=lesson.LessonID).exists():
    profile.CompletedLessons.remove(lesson)
    progressDecrease, levelDownMessage = progress_decrease(profile.pk, 10)
    if progressDecrease==False:
      messages.success(request, (levelDownMessage))

  if profile.CompletedProgrammes.filter(ProgrammeID=programme.ProgrammeID).exists():
    profile.CompletedProgrammes.remove(programme)
    messages.error(request, ("Awww! " + programme.ProgrammeName + " Has Been Unmarked As Completed!"))
    progressDecrease, levelDownMessage = progress_decrease(profile.pk, 15)
    if progressDecrease==False:
      messages.success(request, (levelDownMessage))

  messages.error(request, (lesson.LessonName + " Has Been Unmarked As Learned!"))
  return HttpResponseRedirect('/view_programme/%d'%programme.ProgrammeID)
  # get to return to the same page

# ======================================================================================================================================

def save_programme(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  programme = get_object_or_404(Trick_Programme, ProgrammeID=request.POST.get("programme_id"))
  profile.SavedProgrammes.add(programme)
  messages.info(request, (programme.ProgrammeName + " Has Been Added To Your List Of Saved Programmes!"))
  return redirect('programme-list')

# ======================================================================================================================================

def unsave_programme(request, pk):
  profile = User_Profile.objects.get(User_id=pk)
  programme = get_object_or_404(Trick_Programme, ProgrammeID=request.POST.get("programme_id"))

  if profile.SavedProgrammes.filter(ProgrammeID=programme.ProgrammeID).exists():
    profile.SavedProgrammes.remove(programme)

  messages.error(request, (programme.ProgrammeName + " Has Been Removed From Your List Of Saved Programmes!"))
  return redirect('programme-list')

# ======================================================================================================================================

@permission_required('programme.change_programme', login_url='home')
def update_programme(request, programme_id):
  programme = Trick_Programme.objects.get(pk=programme_id)
  form = ProgrammeForm(request.POST or None, request.FILES or None, instance=programme)
  if form.is_valid():
    form.save()
    messages.success(request, ("Trick Updated Successfuly!"))
    return HttpResponseRedirect('/programme_list')
  return render(request, 'main/update_programme.html', {'programme':programme, 'form':form})

# ======================================================================================================================================

@permission_required('trick.delete_trick', login_url='home')
def delete_programme(request, programme_id):
  programme = Trick_Programme.objects.get(pk=programme_id)
  programme.delete()
  return HttpResponseRedirect('/programme_list')

# ======================================================================================================================================

@permission_required('category.add_category', login_url='home')
def add_category(request):
    submitted = False
    if request.method == "POST":
      form = CategoryForm(request.POST, request.FILES)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect('/add_category?submitted=True')
    else:
      form = CategoryForm
      if 'submitted' in request.GET:
        submitted = True
        messages.success(request, ("New Category Created!"))
    return render(request, 'main/add_category.html', {'form':form, 'submitted':submitted})

# ======================================================================================================================================

def category_list(request):

  all_categories = Category.objects.all().order_by('CategoryID')

  return render(request, 'main/category_list.html', {'categories': all_categories})

# ======================================================================================================================================

def show_category(request, category_id):
  current_page = request.path

  category = Category.objects.get(pk=category_id)
  categoryID = category.CategoryID
  tricks =  Trick.objects.filter(TrickCategory=categoryID).order_by('TrickRecLevel', 'TrickDifficulty', 'TrickName')
  trick_count = tricks.count()
  
  return render(request, 'main/show_category.html', {'category':category, 'tricks':tricks, 'trick_count':trick_count, 'current_page':current_page})

# ======================================================================================================================================

@permission_required('category.change_category', login_url='home')
def update_category(request, category_id):
  category = Category.objects.get(pk=category_id)
  form = CategoryForm(request.POST or None, request.FILES or None, instance=category)
  if form.is_valid():
    form.save()
    messages.success(request, ("Category Updated Successfuly!"))
    return HttpResponseRedirect('/category_list')
  return render(request, 'main/update_category.html', {'category':category, 'form':form})

# ======================================================================================================================================

@permission_required('trick.delete_trick', login_url='home')
def delete_category(request, category_id):
  category = Category.objects.get(pk=category_id)
  category.delete()
  return HttpResponseRedirect('/category_list')

# ======================================================================================================================================

def glossary(request):

  CommonTerms = Glossary_Term.objects.filter(CommonlyUsed=True).order_by('KeyWord')
  UncommonTerms = Glossary_Term.objects.filter(CommonlyUsed=False).order_by('KeyWord')

  CommonTermCount = CommonTerms.count()
  UncommonTermCount = UncommonTerms.count()
  TermCount = CommonTermCount + UncommonTermCount
  
  return render(request, 'main/glossary.html', {'CommonTerms':CommonTerms, 'UncommonTerms':UncommonTerms, 'TermCount':TermCount})

# ======================================================================================================================================

@permission_required('category.add_category', login_url='home')
def add_glossary_term(request):
    submitted = False
    if request.method == "POST":
      form = GlossaryTermForm(request.POST, request.FILES)
      if form.is_valid():
        form.save()
        return HttpResponseRedirect('/add_glossary_term?submitted=True')
    else:
      form = GlossaryTermForm
      if 'submitted' in request.GET:
        submitted = True
        messages.success(request, ("New Term Added To The Glossary!"))
    return render(request, 'main/add_glossary_term.html', {'form':form, 'submitted':submitted})

# ======================================================================================================================================

@login_required(login_url='/login')
def admin_db(request):
  # An Extra Level Security for the Admin Panel
  if request.user.is_superuser :
    return HttpResponseRedirect('/admin')
  else:
    return HttpResponseRedirect('/home')

# ======================================================================================================================================

