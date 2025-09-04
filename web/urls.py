from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("problems/", views.problem_list, name="problem_list"),
    path("problems/<slug>/", views.problem, name="problem"),
    path("accounts/register/", views.RegistrationView.as_view(), name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
]
