# Generated by Django 4.2rc1 on 2023-04-20 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0004_eventroundstate_revealed"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaderboardentry",
            name="megaround_applied",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="leaderboardentry",
            name="selected_megaround",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="questionresponse",
            name="megaround_value",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]