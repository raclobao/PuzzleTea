# Generated by Django 4.2.7 on 2023-12-25 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("PuzzleTeaApp", "0022_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="jigsaw",
            name="product_ptr",
        ),
        migrations.RemoveField(
            model_name="tea",
            name="product_ptr",
        ),
        migrations.DeleteModel(
            name="Cube",
        ),
        migrations.DeleteModel(
            name="Jigsaw",
        ),
        migrations.DeleteModel(
            name="Tea",
        ),
    ]
