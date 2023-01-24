from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model

from .models import Trickster_User, User_Profile

#Universally setting User to get_user_model
#User = get_user_model()


class UserRegistrationForm(UserCreationForm):
  Email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
  FirstName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
  LastName = forms.CharField(max_length=50,  widget=forms.TextInput(attrs={'class':'form-control'}))
  Username = forms.CharField(max_length=50,  widget=forms.TextInput(attrs={'class':'form-control'}))

  class Meta:
      model = Trickster_User
      fields = ('Username','FirstName', 'LastName', 'Email', 'password1', 'password2')

  def __init__(self,  *args, **kwargs):
      super(UserRegistrationForm, self).__init__(*args, **kwargs)

      self.fields['password1'].widget.attrs['class'] = 'form-control'
      self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserAuthenticationForm(forms.ModelForm):

  Email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
  password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

  class Meta:
    model = Trickster_User
    fields = ('Email', 'password')

  def clean(self):
    Email = self.cleaned_data['Email']
    password = self.cleaned_data['password']
    if not authenticate(Email=Email, password=password):
      raise forms.ValidationError("Invalid Login")

class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = User_Profile
    fields = ('ProfilePhoto',)
    labels = {
      'ProfilePhoto':'',
    }

    widgets = {
        'ProfilePhoto': forms.ClearableFileInput(attrs={'class':'form-control'}),
    }

class UserUpdateForm(forms.ModelForm):        
  class Meta:
    model = Trickster_User
    fields = ('Username', 'Email', 'FirstName', 'LastName')
    labels = {
      'Username':'Username',
      'Email':'Email',
      'FirstName':'First Name',
      'LastName':'Last Name'
    }
    widgets = {
      'Username' : forms.TextInput(attrs={'class':'form-control'}),
      'Email' : forms.EmailInput(attrs={'class':'form-control'}),
      'FirstName' : forms.TextInput(attrs={'class':'form-control'}),
      'LastName' : forms.TextInput(attrs={'class':'form-control'})
    }
