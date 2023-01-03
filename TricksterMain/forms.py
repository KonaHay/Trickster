from django import forms
from django.forms import ModelForm
from .models import Trick

#Form to add a trick to the database.
class TrickForm(ModelForm):
    class Meta:
        model = Trick
        fields = ('TrickName', 'TrickRecLevel',  'TrickDifficulty',  'TrickDiscription', 'TrickHowTo', 'TrickImg')

        #Getting errors with the 'attrs' tag. will try and fix ltr.
        widgets = {
            'TrickName': forms.TextInput(widget=forms.FileInput(attrs={'class':'form-control'})),
            'TrickRecLevel': forms.RadioSelect(widget=forms.FileInput(attrs={'class':'form-control'})),
            'TrickDifficulty': forms.TextInput(widget=forms.FileInput(attrs={'class':'form-control'})),
            'TrickDiscription': forms.TextInput(widget=forms.FileInput(attrs={'class':'form-control'})),
            'TrickHowTo': forms.TextInput(widget=forms.FileInput(attrs={'class':'form-control'})),
            'TrickImg': forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'})),
        }
