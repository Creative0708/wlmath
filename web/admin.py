from django.contrib import admin
from django.contrib.admin.sites import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import Problem, WlmathUser, Tag

class WlmathModelAdmin(admin.ModelAdmin):
	class Media:
		css = {
			"all": ("admin.css",)
		}

admin.site.register(WlmathUser, UserAdmin)
admin.site.register(Problem, WlmathModelAdmin)
admin.site.register(Tag, ModelAdmin)
