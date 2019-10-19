from django.shortcuts import render
from .forms import RegistrationForm



def home(request):
  return render(request,'main/home.html')

def register(request):
  reg_form = RegistrationForm()
  return render(request,'auth/registration.html',{'reg_form':reg_form})

