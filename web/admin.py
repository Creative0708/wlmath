from django.contrib import admin
from django.contrib.admin.sites import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import Problem, WlmathUser

admin.site.register(WlmathUser, UserAdmin)
admin.site.register(Problem, ModelAdmin)
