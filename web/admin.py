from django.contrib import admin
from django.contrib.admin.sites import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import Problem, WlmathUser, Tag, WebsiteData, UpcomingContest, PastResource

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

class UpcomingContestAdmin(ModelAdmin):
	list_display = ('name', 'date')
	list_filter = ('date', )

class PastResourcesAdmin(ModelAdmin):
	list_display = ('title', 'date')
	list_filter = ('date', )

admin.site.register(WlmathUser, WlmathUserAdmin)
admin.site.register(Problem, ModelAdmin)
admin.site.register(Tag, ModelAdmin)
admin.site.register(WebsiteData, ModelAdmin)
admin.site.register(UpcomingContest, UpcomingContestAdmin)
admin.site.register(PastResource, PastResourcesAdmin)