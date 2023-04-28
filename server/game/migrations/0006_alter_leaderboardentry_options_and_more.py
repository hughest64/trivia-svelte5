# Generated by Django 4.2rc1 on 2023-04-21 12:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0005_leaderboardentry_megaround_applied_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="leaderboardentry",
            options={
                "ordering": [
                    "event",
                    "rank",
                    "tiebreaker_rank",
                    "team",
                    "-leaderboard_type",
                    "pk",
                ],
                "verbose_name_plural": "Leaderboard Entries",
            },
        ),
        migrations.AlterField(
            model_name="questionresponse",
            name="megaround_value",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="questionresponse",
            name="recorded_answer",
            field=models.TextField(blank=True, default=""),
        ),
    ]
