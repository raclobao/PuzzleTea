# Generated by Django 4.2.7 on 2023-12-26 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("PuzzleTeaApp", "0026_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shippingorder",
            name="warehouse",
        ),
        migrations.AlterField(
            model_name="cube",
            name="product_barcode",
            field=models.OneToOneField(
                db_column="barcode",
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="PuzzleTeaApp.product",
            ),
        ),
        migrations.AlterField(
            model_name="jigsaw",
            name="pieceCount",
            field=models.IntegerField(verbose_name="Piece count"),
        ),
        migrations.AlterField(
            model_name="jigsaw",
            name="product_barcode",
            field=models.OneToOneField(
                db_column="barcode",
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="PuzzleTeaApp.product",
            ),
        ),
        migrations.AlterField(
            model_name="quantity",
            name="product_barcode",
            field=models.ForeignKey(
                db_column="barcode",
                on_delete=django.db.models.deletion.CASCADE,
                to="PuzzleTeaApp.product",
            ),
        ),
        migrations.AlterField(
            model_name="quantity",
            name="shippingorder_orderid",
            field=models.ForeignKey(
                db_column="orderid",
                on_delete=django.db.models.deletion.CASCADE,
                to="PuzzleTeaApp.shippingorder",
            ),
        ),
        migrations.AlterField(
            model_name="shippingorder",
            name="client_clientid",
            field=models.ForeignKey(
                db_column="clientid",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="stock",
            name="product_barcode",
            field=models.ForeignKey(
                db_column="barcode",
                on_delete=django.db.models.deletion.CASCADE,
                to="PuzzleTeaApp.product",
            ),
        ),
        migrations.AlterField(
            model_name="tea",
            name="caffeineLevel",
            field=models.CharField(
                choices=[("1", "Low"), ("2", "Medium"), ("3", "High")],
                default="2",
                verbose_name="Caffeine level",
            ),
        ),
        migrations.AlterField(
            model_name="tea",
            name="product_barcode",
            field=models.OneToOneField(
                db_column="barcode",
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="PuzzleTeaApp.product",
            ),
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "client_clientid",
                    models.ForeignKey(
                        db_column="clientid",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
