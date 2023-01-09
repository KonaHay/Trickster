from django import forms
from django.forms import ModelForm
from .models import Trick

#Form to add a trick to the database.
class TrickForm(ModelForm):
    class Meta:
        model = Trick
        fields = ('TrickName', 'TrickRecLevel',  'TrickDifficulty',  'TrickDiscription', 'TrickHowTo', 'TrickImg')
        labels = {
            'TrickName': 'Enter the Trick Name:',
            'TrickRecLevel':'Reccomended Level for this Trick:',
            'TrickDifficulty':'Trick Difficulty (Scale 1-10):',
            'TrickDiscription':'Enter the discription of this trick:',
            'TrickHowTo':'Enter a How To for this trick:',
            'TrickImg':'Upload a cover image for this trick:',
        }
        
        widgets = {
            'TrickName': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ollie'}),
            'TrickRecLevel': forms.Select(attrs={'class':'form-control', 'placeholder':'Select a skill level'}),
            'TrickDifficulty': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'1'}),
            'TrickDiscription': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter discription here.'}),
            'TrickHowTo': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class':'form-control', 'placeholder':'Enter How To here.'}),
            'TrickImg': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }
