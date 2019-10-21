from django.shortcuts import render,redirect
from .forms import RegistrationForm,PostProjectsForm,ProjectRatingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project,Profile,Tag,Technology,Rating
from django.http import JsonResponse
from django.contrib.auth.models import User



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


@login_required
def vote(request,project_id):
  project = Project.get_project(project_id)
  tags = Project.objects.filter(pk = project_id).first().tag.all()
  rate_form = ProjectRatingForm()
  voters = Rating.objects.filter(project_id = project_id).all()
  context = {
    'project':project,
    'tags':tags,
    'rate_form':rate_form,
    'voters':voters
  }
  return render(request,'main/projectvote.html',context)

@login_required
def rate(request,project_id):
  design = request.POST.get('design')
  usability = request.POST.get('usability')
  creativity = request.POST.get('creativity')
  content = request.POST.get('content')
  project = Project.objects.filter(pk = project_id ).first()
  user = request.user
  avg = Rating.user_average(design,usability,creativity,content)
  print(avg)
  rating = Rating(project = project,user = user,design = design,usability = usability,creativity = creativity,content = content,vote_average = avg)
  rating.save()
  data = {
    'success':'data received'
  }
  return JsonResponse(data)


@login_required
def search(request):
  if 'search_term' in request.GET and request.GET["search_term"]:
    name = request.GET.get('search_term')
    the_project = Project.search_by_title(name)
    context = {
      'the_projects':the_project
    }
    return render(request,'main/search.html',context)
  else:
    return render(request,'main/search.html')