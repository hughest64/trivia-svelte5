# Generated by Django 4.1b1 on 2022-11-19 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("game", "0003_game_question_triviaevent_gameround_gamequestion_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eventquestionstate",
            options={"ordering": ["event", "round_number", "question_number"]},
        ),
        migrations.AlterModelOptions(
            name="eventroundstate",
            options={"ordering": ["event", "round_number"]},
        ),
        migrations.CreateModel(
            name="Location",
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
                ("name", models.CharField(max_length=128)),
                ("address", models.TextField(blank=True, null=True)),
                ("active", models.BooleanField(default=True)),
                (
                    "primary_host",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="triviaevent",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="game.location",
            ),
        ),
    ]
