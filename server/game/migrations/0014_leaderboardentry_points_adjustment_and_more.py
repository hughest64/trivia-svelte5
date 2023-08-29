# Generated by Django 4.2.2 on 2023-07-21 10:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0013_alter_team_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaderboardentry",
            name="points_adjustment",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="leaderboardentry",
            name="points_adjustment_reason",
            field=models.IntegerField(
                choices=[
                    (0, "-----"),
                    (1, "Team Limit Exceeded"),
                    (2, "Best Team Name"),
                    (3, "Funny Answer"),
                    (4, "Team Spirit"),
                    (5, "Host Discretion"),
                ],
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
    ]