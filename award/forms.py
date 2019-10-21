from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Project,Rating


class RegistrationForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['username','email','password1','password2']

class PostProjectsForm(forms.ModelForm):
  class Meta:
    model = Project
    exclude = ['user']
    widgets = {
      'tag': forms.CheckboxSelectMultiple(),
      'technologies':forms.CheckboxSelectMultiple()
    }


class ProjectRatingForm(forms.ModelForm):
  class Meta:
    model = Rating
    exclude = ['user','project','vote_average']

  