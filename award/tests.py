from django.test import TestCase
from .models import Project,Tag,Technology
from django.contrib.auth.models import User


class TestProjectModel(TestCase):
  def setUp(self):
    self.new_tag = Tag(name = "cars")
    self.new_tag.save()
    self.new_tech = Technology(name = "HTML")
    self.new_tech.save()
    self.new_user = User(username = "admin")
    self.new_project = Project(title = "awwards",landing_page = "awards.png",description = "awarding website",live_link = "awards.com",tag = self.new_tag,posted_on = "2019/10/20",catogory = "tech",technologies = self.new_tech,collaborators = "Denis",user = self.new)

