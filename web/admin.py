from django.contrib import admin
from django.contrib.admin.sites import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import Problem, WlmathUser, Tag

class WlmathModelAdmin(admin.ModelAdmin):
	class Media:
		css = {
			"all": ("admin.css",)
		}

class WlmathUserAdmin(UserAdmin):
	model = WlmathUser

	list_display = ("username", "email", "points" , "grade")
	list_filter = ("grade",)

	fieldsets = (
		("Profile", {"fields": ("username", "email", "password", "grade", "bio", "points")}),
	)

	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": ("username", "email", "password1", "password2", "grade"),
		}),
	)

	search_fields = ("username", "email")
	ordering = ("username", "points")

admin.site.register(WlmathUser, WlmathUserAdmin)
admin.site.register(Problem, ModelAdmin)
admin.site.register(Tag, ModelAdmin)
