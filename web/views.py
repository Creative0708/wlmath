from django.contrib.auth import get_user_model
from django import forms
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.contrib.auth.forms import SetPasswordMixin, UserCreationForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.serializers import serialize
from django.db.models import F, Window, Count
from django.db.models.functions import Rank
from django.core.paginator import Paginator
from . import consts
import json

from web.models import Problem
User = get_user_model()

def index(request):
	recent_problems = Problem.objects.order_by("date_added")[:8]
	return render(request, "index.html", { "problems": recent_problems })

def problem(request, slug):
	user = request.user
	problem = get_object_or_404(Problem, slug=slug)
	solved = not user.is_anonymous and user.problems_solved.contains(problem)

	success = False
	if request.method == "POST":
		if user.is_anonymous:
			return HttpResponse(status=403)
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
	answer = forms.CharField(max_length=consts.ANSWER_MAX_LENGTH, widget=forms.TextInput(attrs={ "class": "w-full" }))

	def __init__(self, *args, problem: Problem, **kwargs) -> None:
		self.problem = problem
		super().__init__(*args, **kwargs)

	def clean(self):
		if not self.errors and self.cleaned_data.get("answer") != self.problem.answer:
			self.add_error("answer", f"[testing] answer is {self.problem.answer}")
		return super().clean()

def problem_list(request):
	problems = Problem.objects.order_by("date_added")

	if request.user.is_authenticated:
		problems_solved = request.user.problems_solved.all()
	else:
		problems_solved = set()
	return render(request, "problemlist.html", { "problems": problems, "solved": problems_solved })

def users(request):
	page_limit = 50

	try:
		page = int(request.GET.get('page')) or 1
	except:
		page = 1

	column = request.GET.get('column') or "points"
	order = request.GET.get('order') or "desc"

	if column not in ['points', 'number_of_solved'] or order not in ['asc', 'desc']:
		return redirect(request.path)

	prefix = "-" if order == "desc" else ""

	users = User.objects.annotate(
		number_of_solved=Count("problems_solved"),
		rank=Window(
			expression=Rank(),
			order_by=f"{prefix}{column}"
		)
	).order_by(f"{prefix}{column}")

	paginator = Paginator(users, page_limit)

	if (page > paginator.num_pages or page < 0):
		return redirect(request.path)

	page_obj = paginator.get_page(page)

	page_data = page_obj.object_list.values("username", "points", "id", "number_of_solved", "rank")

	data = {
		"data": page_data,
		"pagination": {
			"page": page,
			"has_next": page_obj.has_next(),
			"has_prev": page_obj.has_previous(),
			"total_items": users.count(),
			"total_pages": paginator.num_pages,
			"start": (int(page) - 1) * page_limit + 1,
			"end": (int(page) - 1) * page_limit + page_data.count(),
		}
	}

	return render(request, "users.html", {
		"data": data,
		"column": column,
		"order": order,
	})

class RegistrationForm(UserCreationForm):
	password1, password2 = SetPasswordMixin.create_password_fields(label2="Confirm")
	class Meta:
		model = User
		fields = ("username",)

class RegistrationView(CreateView):
	form_class = RegistrationForm

	success_url = reverse_lazy("login")
	template_name = "registration/register.html"
