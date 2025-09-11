from django import forms
from django.db import models
from martor.widgets import MartorWidget

class WlmathMartorWidget(MartorWidget):
	class Media:
		js = ["martor-mathjax.js"]

class MartorFormField(forms.CharField):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if not issubclass(self.widget.__class__, WlmathMartorWidget):
			self.widget = WlmathMartorWidget()

class MartorField(models.TextField):
	def formfield(self, **kwargs):
		defaults = {"form_class": MartorFormField}
		defaults.update(kwargs)
		return super().formfield(**defaults)
