from django.shortcuts import render,redirect
from .forms import RegistrationForm,PostProjectsForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project,Profile



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
  projects = Project.query_all()
  context = {
    'reg_form':reg_form,
    'projects':projects
  }
  return render(request,'main/home.html',context)


@login_required
def submit(request):
  reg_form=RegistrationForm()
 
  context = {
    'reg_form':reg_form,
  }
  return render(request,'main/submit.html',context)


@login_required
def post_project(request):
  if request.method == 'POST':
    post_form = PostProjectsForm(request.POST,request.FILES)
    if post_form.is_valid():
      the_post = post_form.save(commit=False)
      the_post.user = request.user
      the_post.save()
      return redirect('home')
  else:
    post_form = PostProjectsForm()
  context = {
    'post_form':post_form,
  }
  return render(request,'main/postproject.html',context)


@login_required
def profile(request):
  profile = Profile.get_user_profile(request.user.id)
  projects = Project.objects.filter(user_id = request.user.id ).all()
  context = {
    'projects':projects
  }
  return render(request,'auth/profile.html',context)
