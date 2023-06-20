# Generated by Django 4.2b1 on 2023-03-23 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="leaderboardentry",
            options={
                "ordering": [
                    "event",
                    "-leaderboard_type",
                    "rank",
                    "tiebreaker_rank",
                    "pk",
                ],
                "verbose_name_plural": "Leaderboard Entries",
            },
        ),
        migrations.AddField(
            model_name="leaderboard",
            name="synced",
            field=models.BooleanField(default=True),
        ),
    ]