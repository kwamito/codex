from django.contrib import admin
from .models import Log, Profile, Comment, Files, Project

# Register your models here.
admin.site.register(Log)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Files)
admin.site.register(Project)