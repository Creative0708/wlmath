from django.db import migrations

def create_tags(apps, schema_editor):
    Tag = apps.get_model("web", "Tag")
    CATEGORIES = [
        ("ALG", "Algebra", "bg-sky-600"),
        ("GEO2D", "2-D Geometry", "bg-fuchsia-600"),
        ("GEO3D", "3-D Geometry", "bg-fuchsia-800"),
        ("CAV", "Calculus and Vectors", "bg-teal-700"),
        ("CAP", "Counting and Probability", "bg-lime-600"),
        ("NT", "Number Theory", "bg-emerald-600"),
        ("OTHER", "Other", "bg-zinc-600"),
        ("EASY", "Easy", "bg-green-600"),
        ("MED", "Medium", "bg-yellow-600"),
        ("HARD", "Hard", "bg-red-700"),
        ("VH", "Very Hard", "bg-purple-900"),
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
