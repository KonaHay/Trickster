from django import forms
from django.forms import ModelForm
from .models import Trick, Trick_Programme, Category

#Form to add a trick to the database.
class TrickForm(ModelForm):
    class Meta:
        model = Trick
        fields = ('TrickName', 'TrickRecLevel',  'TrickDifficulty',  'TrickDiscription', 'TrickHowTo', 'TrickCategory', 'TrickImg')
        labels = {
            'TrickName': 'Enter the Trick Name:',
            'TrickRecLevel':'Reccomended Level for this Trick:',
            'TrickDifficulty':'Trick Difficulty (Scale 1-10):',
            'TrickDiscription':'Enter the discription of this trick:',
            'TrickHowTo':'Enter a How To for this trick:',
            'TrickCategory':'Select a Category for the new Trick:',
            'TrickImg':'Upload a cover image for this trick:',
        }
        
        widgets = {
            'TrickName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ollie'}),
            'TrickRecLevel': forms.Select(attrs={'class':'form-control', 'placeholder':'Select a skill level'}),
            'TrickDifficulty': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1'}),
            'TrickDiscription': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter discription here.'}),
            'TrickHowTo': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter How To here.'}),
            #Change to a select multiple feild.
            #'TrickCategory':forms.CheckboxSelectMultiple(attrs={'class':'form-control', 'placeholder':'Select a skill level'}),
            'TrickImg': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('CategoryName',)
        labels = {
            'CategoryName': 'Enter the Category Name:',
        }
        
        widgets = {
            'CategoryName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cabel Trick'}),
        }

#Form to add a trick programme to the database.
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

