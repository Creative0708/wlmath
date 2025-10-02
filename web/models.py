from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.base import Manager
from django.db.models.functions import Now
from .markdown import MartorField
from . import consts

class WlmathUserManager(UserManager):
	pass

class WlmathUser(AbstractUser):
	objects = WlmathUserManager()

	first_name = None
	last_name = None

	points = models.IntegerField(default=0)
	grade = models.CharField(max_length=20, blank=True)
	bio = models.TextField(max_length=consts.PROFILE_BIO_LIMIT, blank=True)

	problems_solved = models.ManyToManyField('Problem')

	# badges = models.ManyToManyField('Badge', blank=True)

class ProblemManager(Manager):
	pass

class Tag(models.Model):
	contraction = models.CharField(max_length=8, unique=True)
	name = models.CharField(max_length=32)
	color = models.CharField(max_length=16, default="bg-zinc-400")

	def __str__(self):
		return self.name

class Problem(models.Model):
	objects = ProblemManager()

	title = models.CharField(max_length=64)
	body = MartorField()
	slug = models.CharField(max_length=16)

	answer = models.CharField(max_length=consts.ANSWER_MAX_LENGTH)
	points = models.IntegerField()
	tags = models.ManyToManyField(Tag, related_name="problems")

	date_added = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)


	def url(self):
		return f"/problems/{self.slug}/"

	def __str__(self):
		return self.title
