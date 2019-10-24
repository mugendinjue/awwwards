from django.urls import path,re_path
from . import views as main_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import models

urlpatterns = [
  path('home',main_views.home,name='home'),
  path('',main_views.register,name='register'),
  path('login/',auth_views.LoginView.as_view(template_name = 'auth/login.html'),name = 'login'),
  path('logout/',auth_views.LogoutView.as_view(template_name = 'auth/logout.html'),name='logout'),
  path('submission',main_views.submit,name='submissions'),
  path('postform/',main_views.post_project, name='postform'),
  path('profile/',main_views.profile, name='profile'),
  re_path(r'^vote/(?P<project_id>\d+)$',main_views.vote, name='vote'),
  re_path(r'^rating/data/(?P<project_id>\d+)$',main_views.rate,name='rate'),
  re_path(r'^search/$',main_views.search,name='search'),
  re_path(r'^api/projects/$', main_views.ProjectList.as_view()),
  re_path(r'^api/profiles/$', main_views.ProfileList.as_view()),
  path('developers/',main_views.developers, name='developers'),
]

if settings.DEBUG:
  urlpatterns+= static(
    settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
  )