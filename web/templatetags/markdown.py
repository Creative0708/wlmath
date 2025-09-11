from django import template
from django.utils.safestring import mark_safe
from l2m4m import LaTeX2MathMLExtension
import markdown, nh3, json
from os import path

md = markdown.Markdown(
	extensions=[
		LaTeX2MathMLExtension(),
	],
)
with open(path.join(path.dirname(__file__), "allowed_tags.json")) as f:
	sanitizer = nh3.Cleaner(tags=set(json.loads(f.read())))

register = template.Library()
@register.filter
def markdownify(text):
	assert text is not None
	md.reset()
	html = md.convert(text)
	html = sanitizer.clean(html)

	return mark_safe(html)
