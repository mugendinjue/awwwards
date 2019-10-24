from rest_framework import serializers
from .models import Project,Tag,Technology,Rating,Profile
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['name']

class TechnologySerializer(serializers.ModelSerializer):
  class Meta:
    model = Technology
    fields = ['name']

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username']

class RatingSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  class Meta:
    model = Rating
    fields = ['user','design','usability','creativity','content','vote_average']



class ProjectSerializer(serializers.ModelSerializer):
  tag = TagSerializer(many=True,read_only=True)
  technologies = TechnologySerializer(many=True,read_only=True)
  person_rating = UserSerializer(read_only=True)
  project_rating = RatingSerializer(many=True,read_only=True)
  class Meta:
    model = Project
    fields = ['title','description','live_link','tag','landing_page','posted_on','category','technologies','Collaborators','person_rating','project_rating']



    # Profile api secction


class ProfileSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  class Meta:
    model = Profile
    fields = ['user','profile_pic','bio','nationality']