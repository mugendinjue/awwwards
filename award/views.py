from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def register(request):
  if request.method == 'POST':
    reg_form = RegistrationForm(request.POST)
    if reg_form.is_valid():
      reg_form.save()
      username = reg_form.cleaned_data.get('username')
      messages.success(request,f'Account for {username} has been created successfully.You can proceed to login')
      return redirect('login')
  else:
    reg_form=RegistrationForm()
      
  return render(request,'auth/registration.html',{'reg_form':reg_form})


@login_required
def home(request):
  reg_form=RegistrationForm()
  return render(request,'main/home.html',{'reg_form':reg_form})


@login_required
def submit(request):
  reg_form=RegistrationForm()
  return render(request,'main/submit.html',{'reg_form':reg_form})

