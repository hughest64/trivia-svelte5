# Generated by Django 4.2.2 on 2023-08-16 12:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0021_alter_team_name_alter_team_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="question_notes",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
