from django.shortcuts import render,redirect
from .forms import RegistrationForm,PostProjectsForm,ProjectRatingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project,Profile,Tag,Technology,Rating
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectSerializer,ProfileSerializer
from rest_framework import status



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
  
  top = []
  for project in projects:
    project_points = Rating.objects.filter(project_id = project.id).all()
    arr = []
    for point in project_points:
      arr.append(point.vote_average)
      avg = sum(arr)/len(arr)
      top.append(avg)

  show_top = (max(top))
     

  for project in projects:
    project_points = Rating.objects.filter(project_id = project.id).all()
    arr = []
    for point in project_points:
      arr.append(point.vote_average)
      avg = sum(arr)/len(arr)
      if avg == show_top:
        tt = point.id

  the_sod = []
  for project in projects:
    project_points = Rating.objects.filter(project_id = project.id).all()
    arr = []
    for point in project_points:
      arr.append(point.vote_average)
      avg = sum(arr)/len(arr)
      if avg >= 7 :
        sod = point.id
        the_sod.append(sod)


  site_of_day = []
  for i in the_sod:
    sod_projects = Rating.objects.filter(id = i)
    for sooood in sod_projects:
        site_of_day.append(Project.objects.filter(id = sooood.project_id))


  the_project = Rating.objects.get(id = tt)
  get_projects = Rating.objects.filter(project_id = the_project.project_id).all()

  design = []
  for de in get_projects:
    design.append(de.design)
  design_avg = sum(design)/len(design)

  userbility = []
  for de in get_projects:
    userbility.append(de.usability)
  userbility_avg = sum(userbility)/len(userbility)

  creativity = []
  for de in get_projects:
    creativity.append(de.creativity)
  creativity_avg = sum(creativity)/len(creativity)

  content = []
  for de in get_projects:
    content.append(de.content)
  content_avg = sum(content)/len(content)
  context = {
    'reg_form':reg_form,
    'projects':projects,
    'the_project':the_project,
    'show_top':show_top,
    'design_avg':str(design_avg),
    'userbility_avg':str(userbility_avg),
    'creativity_avg':str(creativity_avg),
    'content_avg':str(content_avg),
    'site_of_day':site_of_day,

  }
  return render(request,'main/home.html',context)


class ProjectList(APIView):
  def get(self, request, format=None):
    all_projects = Project.objects.all()
    serializers = ProjectSerializer(all_projects, many=True)
    return JsonResponse(serializers.data,safe=False)

class ProfileList(APIView):
  def get(self,request,format=None):
    all_profiles = Profile.objects.all()
    serializers = ProfileSerializer(all_profiles,many=True)
    return JsonResponse(serializers.data,safe=False)

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
  return render(request,'main/profile.html',context)


def developers(request):
  return render(request,'main/developers.html')


@login_required
def vote(request,project_id):
  project = Project.get_project(project_id)
  tags = Project.objects.filter(pk = project_id).first().tag.all()
  rate_form = ProjectRatingForm()
  voters = Rating.objects.filter(project_id = project_id).all()
  project_points = Rating.objects.filter(project_id = project_id).all()
  arr = []
  for point in project_points:
    arr.append(point.vote_average)

  arr_length = len(arr)
  if arr_length == 0:
    arr_length = 1
    avg = sum(arr)/arr_length
  else:
    avg = sum(arr)/len(arr)
  context = {
    'project':project,
    'tags':tags,
    'rate_form':rate_form,
    'voters':voters,
    'avg':avg
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
  rater  = Rating.objects.filter(user_id = user.id,project_id = project.id).first()
  if rater is not None:
    old_rating = Rating.objects.filter(user_id = user.id).all()
    old_rating.delete()
    rating = Rating(project = project,user = user,design = design,usability = usability,creativity = creativity,content = content,vote_average = avg)
    rating.save()
  else:
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