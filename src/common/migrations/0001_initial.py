# Generated by Django 4.1.7 on 2023-04-01 11:48

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AddEbookModel",
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
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                ("ebook_title", models.CharField(max_length=512)),
                ("ebook_link", models.URLField()),
                ("full_name", models.CharField(max_length=128)),
                ("email", models.EmailField(max_length=254)),
                ("checked", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BlogModel",
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
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                ("title", models.CharField(max_length=512)),
                ("description", ckeditor.fields.RichTextField()),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=512, null=True, unique=True
                    ),
                ),
                ("views_count", models.PositiveIntegerField(default=0)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
