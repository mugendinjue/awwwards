from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.dispatch import receiver
from django.db.models.signals import post_save


class Tag(models.Model):
  name = models.CharField(max_length=20)

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
  tag = models.ManyToManyField(Tag)
  posted_on = models.DateTimeField(auto_now_add=True)
  category = models.CharField(max_length=50,blank=True)
  technologies = models.ManyToManyField(Technology)
  user = models.ForeignKey(User,on_delete=models.CASCADE)


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


  def __str__(self):
    return "%s profile"%self.user


class Rating(models.Model):
  project = models.ForeignKey(Project,on_delete = models.CASCADE,related_name='project_rating')
  user = models.ForeignKey(User,on_delete = models.CASCADE,related_name='person_rating')
  design = models.IntegerField()
  usability = models.IntegerField()
  creativity = models.IntegerField()
  content = models.IntegerField()


  def __str__(self):
    return "%s rate"%self.project


