from django.contrib.auth import get_user_model
from django import forms
from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.contrib.auth.forms import SetPasswordMixin, UserCreationForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import F, Window, Count
from django.db.models.functions import Rank
from django.core.paginator import Paginator
from django.utils import timezone
from . import consts
from hashlib import sha256

from web.models import Problem, WebsiteData, UpcomingContest, PastResources
User = get_user_model()


def index(request):
	recent_problems = Problem.objects.order_by("date_added")[:8]

	return render(request, "index.html", {"problems": recent_problems})


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
			self.add_error("answer", f"That's not the right answer.")
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
	password1, password2 = SetPasswordMixin.create_password_fields(
		label2="Confirm")

	class Meta:
		model = User
		fields = ("username",)


class RegistrationView(CreateView):
	form_class = RegistrationForm

	success_url = reverse_lazy("login")
	template_name = "registration/register.html"

class EditUserProfile(forms.Form):
	bio = forms.CharField(max_length=consts.PROFILE_BIO_LIMIT,
							 widget=forms.Textarea(attrs={"class": "w-full border border-wlblue p-2 rounded-sm focus:outline-none"}))

	grade = forms.CharField(max_length=20,
							 widget=forms.TextInput(attrs={"class": "w-30 !border-wlblue border px-2 rounded-sm focus:outline-none"}))

	def __init__(self, *args, **kwargs) -> None:
		user_data = kwargs.pop('user_data', None)
		super().__init__(*args, **kwargs)

		if user_data:
			self.fields['bio'].initial = user_data['bio']
			self.fields['grade'].inital_grade = user_data['grade']

def user_self_edit(request):

	req_user = request.user

	if not req_user.is_authenticated:
		return redirect(reverse_lazy('login'))

	profile = get_object_or_404(User, username=req_user.username)
	email_hash = sha256(profile.email.encode('utf-8')).hexdigest()

	if request.method == "POST":
		form = EditUserProfile(request.POST)
		if form.is_valid():
			profile.bio = form.cleaned_data['bio']
			profile.grade = form.cleaned_data['grade']
			profile.save()

			return redirect(reverse_lazy('profile_self'))
	else:
		form = EditUserProfile(user_data={
			"bio": profile.bio,
			"grade": profile.grade
		})

	return render(request, "user_edit.html", {
		"bio": profile.bio,
		"grade": profile.grade,
		"username": profile.username,
		"email_hash": email_hash,
		"form": form
	})

def user_self(request):

	req_user = request.user

	if not req_user.is_authenticated:
		return redirect(reverse_lazy('login'))

	return user(request, req_user.username, True)


def user(request, username, is_self=False):

	profile = get_object_or_404(User, username=username)

	email_hash = sha256(profile.email.encode('utf-8')).hexdigest()
	num_problems_solved = profile.problems_solved.count()
	rank = User.objects.filter(points__gt=profile.points).count() + 1
	problems_solved = profile.problems_solved.all().order_by("-points")[:25]

	grade = profile.grade

	if grade == "" or grade == None:
		grade = "N/A"

	return render(request, "user.html", {
		"username": username,
		"email_hash": email_hash,
		"num_problems_solved": num_problems_solved,
		"grade": grade,
		"points": profile.points,
		"rank": rank,
		"problems_solved": problems_solved,
		"bio": profile.bio,
		"is_self": is_self
	})

def user_self_problems(request):

	req_user = request.user

	if not req_user.is_authenticated:
		return redirect(reverse_lazy('login'))

	return user_problems(request, req_user.username)


def user_problems(request, username):

	profile = get_object_or_404(User, username=username)

	email_hash = sha256(profile.email.encode('utf-8')).hexdigest()
	problems_solved = profile.problems_solved.all().order_by("-points")

	return render(request, "user_problems.html", {
		"username": username,
		"email_hash": email_hash,
		"points": profile.points,
		"problems_solved": problems_solved,
	})

def resources(request):
	content = WebsiteData.objects.get(data_id="resources") or ""
	contest_data = UpcomingContest.objects.filter(date__gt=timezone.now()).order_by("date")
	lessons = PastResources.objects.filter(date__lt=timezone.now()).order_by("date")

	return render(request, "resources.html", {
		"contest_data": contest_data,
		"lesson_data": [lesson.__dict__ | {'index': i + 1} for i, lesson in enumerate(lessons)],
		"general_resources": content
	})