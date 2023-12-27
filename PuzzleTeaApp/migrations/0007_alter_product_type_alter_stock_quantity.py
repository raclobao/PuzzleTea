# Generated by Django 4.2.7 on 2023-12-21 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PuzzleTeaApp", "0006_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="type",
            field=models.CharField(
                choices=[("twist", "TwistyPuzzle"), ("tea", "Tea"), ("jig", "JigSaw")],
                default="jig",
            ),
        ),
        migrations.AlterField(
            model_name="stock",
            name="quantity",
            field=models.IntegerField(default=0),
        ),
    ]
