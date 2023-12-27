# Generated by Django 4.2.7 on 2023-12-21 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("PuzzleTeaApp", "0010_remove_cube_product_ptr_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
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
                ("name", models.CharField()),
                ("address", models.CharField()),
            ],
            options={
                "db_table": "client",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("barcode", models.IntegerField(primary_key=True, serialize=False)),
                ("type", models.CharField()),
                ("name", models.CharField()),
            ],
            options={
                "db_table": "product",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Warehouse",
            fields=[
                ("name", models.CharField(primary_key=True, serialize=False)),
                ("address", models.CharField(unique=True)),
            ],
            options={
                "db_table": "warehouse",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Cube",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="PuzzleTeaApp.product",
                    ),
                ),
                ("size", models.CharField(blank=True, null=True)),
                ("weight", models.FloatField()),
            ],
            options={
                "db_table": "cube",
                "managed": True,
            },
            bases=("PuzzleTeaApp.product",),
        ),
        migrations.CreateModel(
            name="Jigsaw",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="PuzzleTeaApp.product",
                    ),
                ),
                ("pieces", models.IntegerField()),
            ],
            options={
                "db_table": "jigsaw",
                "managed": True,
            },
            bases=("PuzzleTeaApp.product",),
        ),
        migrations.CreateModel(
            name="Tea",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="PuzzleTeaApp.product",
                    ),
                ),
                ("flavor", models.CharField()),
            ],
            options={
                "db_table": "tea",
                "managed": True,
            },
            bases=("PuzzleTeaApp.product",),
        ),
        migrations.CreateModel(
            name="Shippingorder",
            fields=[
                ("orderid", models.BigIntegerField(primary_key=True, serialize=False)),
                ("orderdate", models.DateField()),
                ("shippingadress", models.CharField()),
                ("warehouse", models.CharField()),
                (
                    "client_clientid",
                    models.ForeignKey(
                        db_column="client_clientid",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="PuzzleTeaApp.client",
                    ),
                ),
            ],
            options={
                "db_table": "shippingorder",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Quantity",
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
                ("quantity", models.IntegerField()),
                (
                    "product_barcode",
                    models.ForeignKey(
                        db_column="product_barcode",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="PuzzleTeaApp.product",
                    ),
                ),
                (
                    "shippingorder_orderid",
                    models.ForeignKey(
                        db_column="shippingorder_orderid",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="PuzzleTeaApp.shippingorder",
                    ),
                ),
            ],
            options={
                "db_table": "quantity",
                "managed": True,
                "unique_together": {("shippingorder_orderid", "product_barcode")},
            },
        ),
        migrations.CreateModel(
            name="Stock",
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
                ("batchid", models.CharField(unique=True)),
                ("quantity", models.IntegerField(default=0)),
                (
                    "product_barcode",
                    models.ForeignKey(
                        db_column="product_barcode",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="PuzzleTeaApp.product",
                    ),
                ),
                (
                    "warehouse_name",
                    models.ForeignKey(
                        db_column="warehouse_name",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="PuzzleTeaApp.warehouse",
                    ),
                ),
            ],
            options={
                "db_table": "stock",
                "managed": True,
                "unique_together": {("batchid", "product_barcode", "warehouse_name")},
            },
        ),
        migrations.CreateModel(
            name="Internalshipping",
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
                ("originwarehouse", models.CharField()),
                ("batchid", models.IntegerField()),
                ("finalwarehouse", models.CharField()),
                ("quantity", models.IntegerField()),
                ("quantity_product_barcode", models.IntegerField()),
                (
                    "quantity_shippingorder_orderid",
                    models.ForeignKey(
                        db_column="quantity_shippingorder_orderid",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="PuzzleTeaApp.quantity",
                    ),
                ),
                (
                    "shippingorder_orderid",
                    models.ForeignKey(
                        db_column="shippingorder_orderid",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="PuzzleTeaApp.shippingorder",
                    ),
                ),
            ],
            options={
                "db_table": "internalshipping",
                "managed": True,
                "unique_together": {("shippingorder_orderid", "batchid")},
            },
        ),
    ]
