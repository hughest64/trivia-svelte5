# Generated by Django 4.2.5 on 2023-10-19 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0033_rename_chanelog_changelog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="changelog",
            name="version",
            field=models.CharField(max_length=120, unique=True),
        ),
    ]