from django.db import migrations

def create_tags(apps, schema_editor):
    Tag = apps.get_model("web", "Tag")
    CATEGORIES = [
        ("Algebra", "Algebra", "#0284c7"),
        ("Geo2D", "2-D Geometry", "#c026d3"),
        ("Geo3D", "3-D Geometry", "#86198f"),
        ("Calculus", "Calculus", "#0f766e"),
        ("Combo", "Combinatorics", "#65a30d"),
        ("N. Theory", "Number Theory", "#059669"),
        ("Ad Hoc", "Ad Hoc", "#52525b"),
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
