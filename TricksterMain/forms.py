from django import forms
from django.forms import ModelForm
from .models import Trick, Trick_Programme, Category, Programme_Lesson, Glossary_Term

class TrickForm(ModelForm):
  class Meta:
    model = Trick
    fields = ('TrickName', 'TrickRecLevel',  'TrickDifficulty',  'TrickDiscription', 'TrickHowTo', 'TrickCategory', 'TrickImg', 'approved')
    labels = {
      'TrickName': 'Enter the Trick Name:',
      'TrickRecLevel':'Reccomended Level for this Trick:',
      'TrickDifficulty':'Trick Difficulty (Scale 1-10):',
      'TrickDiscription':'Enter the discription of this trick:',
      'TrickHowTo':'Enter a How To for this trick:',
      'TrickCategory':'Select a Category for the new Trick (CTRL Click to Add Multiple):',
      'TrickImg':'Upload a cover image for this trick:',
      'approved':'Approved:'
    }
      
    widgets = {
      'TrickName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ollie'}),
      'TrickRecLevel': forms.Select(attrs={'class':'form-control', 'placeholder':'Select a skill level'}),
      'TrickDifficulty': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1'}),
      'TrickDiscription': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter discription here.'}),
      'TrickHowTo': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter How To here.'}),
      #Fix select multiple feild.
      #'TrickCategory':forms.CheckboxSelectMultiple(attrs={'class':'form-check-input', 'type':'checkbox'}),
      'TrickImg': forms.ClearableFileInput(attrs={'class':'form-control'}),
      'approved': forms.CheckboxInput(attrs={"class": "form-check-input"}),
    }

class SubmitTrickForm(ModelForm):
  class Meta:
    model = Trick
    fields = ('TrickName', 'TrickRecLevel',  'TrickDifficulty',  'TrickDiscription', 'TrickHowTo', 'TrickCategory', 'TrickImg')
    labels = {
      'TrickName': 'Enter the Trick Name:',
      'TrickRecLevel':'Reccomended Level for this Trick:',
      'TrickDifficulty':'Trick Difficulty (Scale 1-10):',
      'TrickDiscription':'Enter the discription of this trick:',
      'TrickHowTo':'Enter a How To for this trick:',
      'TrickCategory':'Select a Category for the new Trick (CTRL Click to Add Multiple):',
      'TrickImg':'Upload a cover image for this trick:',
    }
      
    widgets = {
      'TrickName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ollie'}),
      'TrickRecLevel': forms.Select(attrs={'class':'form-control', 'placeholder':'Select a skill level'}),
      'TrickDifficulty': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1'}),
      'TrickDiscription': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter discription here.'}),
      'TrickHowTo': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter How To here.'}),
      #Fix select multiple feild.
      #'TrickCategory':forms.CheckboxSelectMultiple(attrs={'class':'form-check-input', 'type':'checkbox'}),
      'TrickImg': forms.ClearableFileInput(attrs={'class':'form-control'}),
    }

class CategoryForm(ModelForm):
  class Meta:
    model = Category
    fields = ('CategoryName', 'CategoryDescription', 'CategoryImg')
    labels = {
      'CategoryName': 'Enter the Category Name:',
      'CategoryDescription':'Enter the discription of this category:',
      'CategoryImg':'Upload a cover image for this category:',
    }
    
    widgets = {
      'CategoryName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cabel Trick'}),
      'CategoryDescription': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter discription here.'}),
      'CategoryImg': forms.ClearableFileInput(attrs={'class':'form-control'}),
    }

class ProgrammeForm(ModelForm):
  class Meta:
    model = Trick_Programme
    fields = ('ProgrammeName', 'ProgrammeRecLevel',  'ProgrammeDifficulty',  'ProgrammeDiscription', 'ProgrammeImg')
    labels = {
      'ProgrammeName': 'Enter the Programme Name:',
      'ProgrammeRecLevel':'Reccomended Level for this programme:',
      'ProgrammeDifficulty':'Programme Difficulty (Scale 1-10):',
      'ProgrammeDiscription':'Enter the discription of this programme:',
      'ProgrammeImg':'Upload a cover image for this programme:',
    }
    
    widgets = {
      'ProgrammeName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Beginner Guide'}),
      'ProgrammeRecLevel': forms.Select(attrs={'class':'form-control', 'empty_label':'Select a skill level'}),
      'ProgrammeDifficulty': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1'}),
      'ProgrammeDiscription': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter discription here.'}),
      'ProgrammeImg': forms.ClearableFileInput(attrs={'class':'form-control'}),
    }

class LessonForm(ModelForm):
  class Meta:
    model = Programme_Lesson
    fields = ('LessonName', 'LessonNumber', 'LessonShortDesc',  'LessonLongDesc',  'LessonVideo')
    labels = {
      'LessonName': 'Enter the Lesson Name:',
      'LessonNumber': 'Select the Lesson Number:',
      'LessonShortDesc':'Enter the Short Description for this Lesson:',
      'LessonLongDesc':'Enter the Long Description for this Lesson:',
      'LessonVideo':'Add a link to the Lesson Video:',
    }
    
    widgets = {
      'LessonName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Lesson Title'}),
      'LessonNumber': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1'}),
      'LessonShortDesc': forms.Textarea(attrs={'rows': 5, 'cols': 20, 'class':'form-control', 'placeholder':'Enter Short Discription Here.'}),
      'LessonLongDesc': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter Long Discription Here.'}),
      'LessonVideo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Video URL'}),
    }

class GlossaryTermForm(ModelForm):
  class Meta:
    model = Glossary_Term
    fields = ('KeyWord', 'Description', 'CommonlyUsed')
    labels = {
      'KeyWord': 'Enter The Term For The Glossary:',
      'Description':'Enter The Deffinition Of This Term:',
      'CommonlyUsed':'Is This Term Considered Commonly Used:',
    }
    
    widgets = {
      'KeyWord': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cabel Trick'}),
      'Description': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter discription here.'}),
      'CommonlyUsed': forms.CheckboxInput(attrs={"class": "form-check-input"}),
    }
