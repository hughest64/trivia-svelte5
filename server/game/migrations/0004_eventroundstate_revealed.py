# Generated by Django 4.2rc1 on 2023-04-10 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0003_alter_leaderboardentry_options_leaderboard_synced"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventroundstate",
            name="revealed",
            field=models.BooleanField(default=False),
        ),
    ]
