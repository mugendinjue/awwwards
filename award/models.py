from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.dispatch import receiver
from django.db.models.signals import post_save


class Tag(models.Model):
  name = models.CharField(max_length=20)
  

  @property
  def all_tags(self):
    return self.tags.all()

  def __str__(self):
    return "%s tag"%self.name

class Technology(models.Model):
  name = models.CharField(max_length=40)

  def __str__(self):
    return "%s tech"%self.name


class Project(models.Model):
  title = models.CharField(max_length=60)
  landing_page = models.ImageField(upload_to='uploads/')
  description = models.TextField()
  live_link = models.TextField()
  tag = models.ManyToManyField(Tag,related_name='tags')
  posted_on = models.DateTimeField(auto_now_add=True)
  category = models.CharField(max_length=50,blank=True)
  technologies = models.ManyToManyField(Technology,related_name='technologies')
  Collaborators = models.CharField(max_length=100,blank=True)
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  

  @classmethod
  def query_all(cls):
    return cls.objects.all()

  @classmethod
  def get_project(cls,project_id):
    project = cls.objects.get(pk = project_id)
    return project

  @property
  def all_voters(self):
    return self.project_rating.all()

  @classmethod
  def search_by_title(cls,search_term):
    projects = cls.objects.filter(title__icontains = search_term)
    return projects


  def __str__(self):
    return "%s project"%self.title


class Profile(models.Model):
  profile_pic = models.ImageField(default='default.jpg',upload_to='profile/')
  bio = models.TextField()
  user = models.OneToOneField(User,on_delete=models.CASCADE)
  phone_number = models.IntegerField(default='0700000000')
  nationality = models.CharField(max_length=40)

  @receiver(post_save,sender = User)
  def create_profile(instance,sender,created,**kwargs):
    if created:
      Profile.objects.create(user = instance)

  @receiver(post_save,sender = User)
  def save_profile(sender,instance,**kwargs):
    instance.profile.save()


  @classmethod
  def get_user_profile(cls,user_id):
    profile = cls.objects.get(pk=user_id)
    return profile


  def __str__(self):
    return "%s profile"%self.user


class Rating(models.Model):
  project = models.ForeignKey(Project,on_delete = models.CASCADE,related_name='project_rating')
  user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='person_rating')
  design = models.IntegerField()
  usability = models.IntegerField()
  creativity = models.IntegerField()
  content = models.IntegerField()
  vote_average = models.IntegerField()

  def user_average(design,usability,creativity,content):
    summation = int(design)+int(usability)+int(creativity)+int(content)
    average = summation/4
    return average

  def __str__(self):
    return "%s rate"%self.project


