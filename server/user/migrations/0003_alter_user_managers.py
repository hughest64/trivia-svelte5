# Generated by Django 4.2.1 on 2023-06-22 14:38

from django.db import migrations
import user.models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_user_home_location"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", user.models.CustomUserManager()),
            ],
        ),
    ]