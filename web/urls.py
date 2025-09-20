from django.urls import path, include
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("users/", views.users, name="users"),
	path("problems/", views.problem_list, name="problem_list"),
	path("problems/<slug>/", views.problem, name="problem"),
	path("accounts/register/", views.RegistrationView.as_view(), name="register"),
	path("accounts/", include("django.contrib.auth.urls")),
	path("user/<str:username>/problems", views.user_problems, name="profile_problems"),
	path("user/problems", views.user_self_problems, name="profile_self_problems"),
  	path("user/edit", views.user_self_edit, name="profile_self_edit"),
	path("user/<str:username>/", views.user, name="profile"),
	path("user/", views.user_self, name="profile_self"),
	path("martor/", include("martor.urls")),
    path("resources/", views.resources, name="resources")
]
