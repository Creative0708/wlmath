from django.contrib.auth import get_user_model
from django import forms
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.contrib.auth.forms import SetPasswordMixin, UserCreationForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import consts

from web.models import Problem
User = get_user_model()

def index(request):
	recent_problems = Problem.objects.order_by("date_added")[:8]
	return render(request, "index.html", { "problems": recent_problems })

def problem(request, slug):
	problem = get_object_or_404(Problem, slug=slug)
	solved = request.user.problems_solved.contains(problem)

	success = False
	if request.method == "POST":
		form = SubmitProblemForm(request.POST, problem=problem)
		if form.is_valid():
			success = True
			if not solved:
				request.user.problems_solved.add(problem)
	else:
		form = SubmitProblemForm(problem=problem)
	return render(request, "problem.html", {
		"problem": problem,
		"form": form,
		"success": success,
		"solved": solved,
	})

class SubmitProblemForm(forms.Form):
	answer = forms.CharField(max_length=consts.ANSWER_MAX_LENGTH)

	def __init__(self, *args, problem: Problem, **kwargs) -> None:
		self.problem = problem
		super().__init__(*args, **kwargs)

	def clean(self):
		if not self.errors and self.cleaned_data.get("answer") != self.problem.answer:
			self.add_error("answer", f"Wrong answer. (Hint: it's {self.problem.answer})")
		return super().clean()

def problem_list(request):
	problems = Problem.objects.order_by("date_added")
	return render(request, "problemlist.html", { "problems": problems })

class RegistrationForm(UserCreationForm):
	password1, password2 = SetPasswordMixin.create_password_fields(label2="Confirm")
	class Meta:
		model = User
		fields = ("username",)

class RegistrationView(CreateView):
	form_class = RegistrationForm

	success_url = reverse_lazy("login")
	template_name = "registration/register.html"
