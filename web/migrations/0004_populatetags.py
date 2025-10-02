from django.db import migrations

def create_tags(apps, schema_editor):
    Tag = apps.get_model("web", "Tag")
    CATEGORIES = [
    ("ALG", "Algebra", "#0284c7"),        
    ("GEO2D", "2-D Geometry", "#c026d3"), 
    ("GEO3D", "3-D Geometry", "#86198f"), 
    ("CAV", "Calculus and Vectors", "#0f766e"), 
    ("CAP", "Counting and Probability", "#65a30d"), 
    ("NT", "Number Theory", "#059669"),   
    ("OTHER", "Other", "#52525b"),        
    ("EASY", "Easy", "#16a34a"),          
    ("MED", "Medium", "#ca8a04"),         
    ("HARD", "Hard", "#b91c1c"),          
    ("VH", "Very Hard", "#581c87"),       
]

    for code, name, color in CATEGORIES:
        tag, created = Tag.objects.get_or_create(
            contraction=code,
            defaults={"name": name, "color": color},
        )
        if not created:
            tag.name = name
            tag.color = color
            tag.save()


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0001_initial"),  
        ("web", "0002_wlmathuser_bio"),  
        ("web", "0003_tag_color"),  
        
    ]

    operations = [
        migrations.RunPython(create_tags),
    ]
