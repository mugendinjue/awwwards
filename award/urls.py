from django.urls import path
from . import views as main_views


urlpatterns = [
  path('',main_views.home,name='home'),
  path('register/',main_views.register,name='register'),
]