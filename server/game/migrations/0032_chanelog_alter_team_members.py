# Generated by Django 4.2.5 on 2023-10-19 10:35

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("game", "0031_rename_gamequestionnote_teamnote"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChaneLog",
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
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("title", models.CharField(max_length=120)),
                ("version", models.CharField(max_length=120)),
                ("notes", models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name="team",
            name="members",
            field=models.ManyToManyField(
                blank=True, related_name="teams", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
