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

class WebsiteData(models.Model):
	data_id = models.CharField(max_length=100)
	content_markdown = MartorField()

	# Maybe some day you can also add html
	# content_html = models.TextField()

	# use_markdown = models.BooleanField(default=True)
	# use_html = models.BooleanField(default=False)

	def __str__(self):
		return self.data_id
	
class UpcomingContest(models.Model):
	name = models.CharField()
	date = models.DateField()
	contest_link = models.CharField()

	registration_link = models.CharField()
	registration_open = models.BooleanField(default=False)


	def __str__(self):
		return self.name
	
class PastResources(models.Model):
	title = models.CharField()
	date = models.DateField()
	description = models.TextField(blank=True, default="")

	links = models.JSONField(blank=True, default=dict)

	def __str__(self):
		length = 40
		return self.title if len(self.title) <= length else self.title[:length - 3] + "..." 