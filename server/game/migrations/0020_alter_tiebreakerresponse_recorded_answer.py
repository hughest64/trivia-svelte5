# Generated by Django 4.2.2 on 2023-08-10 13:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0019_leaderboardentry_tiebreaker_round_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tiebreakerresponse",
            name="recorded_answer",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
