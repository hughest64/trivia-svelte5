# Generated by Django 4.2.5 on 2023-10-19 10:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0032_chanelog_alter_team_members"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ChaneLog",
            new_name="ChangeLog",
        ),
    ]
