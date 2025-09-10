from django.core.management.base import BaseCommand
from web.models import Tag

TAGS = [
    ("ALG", "Algebra"),
    ("GEO2D", "2D Geometry"),
    ("GEO3D", "3D Geometry"),
    ("CAV", "Calculus and Vectors"),
    ("CAP", "Counting and Probability"),
    ("NT", "Number Theory"),
    ("OTHER", "Other"),
    ("EZ", "Easy"),
    ("MD", "Medium"),
    ("HD", "Hard"),
    ("VH", "Very Hard")
]

class Command(BaseCommand):
    help = "populate default tags"  
    
    def handle(self, *args, **kwargs):
        for contraction, name in TAGS:
            Tag.objects.get_or_create(contraction=contraction, name=name)
        self.stdout.write(self.style.SUCCESS("categories populated"))