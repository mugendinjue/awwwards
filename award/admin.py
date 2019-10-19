from django.contrib import admin
from .models import Rating,Tag,Technology,Profile,Project

admin.site.register(Profile)
admin.site.register(Rating)
admin.site.register(Project)
admin.site.register(Technology)
admin.site.register(Tag)
