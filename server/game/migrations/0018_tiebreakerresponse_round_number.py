# Generated by Django 4.2.2 on 2023-07-27 14:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0017_remove_tiebreakerresponse_leaderboard_entry_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tiebreakerresponse",
            name="round_number",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]