# Generated by Django 4.1b1 on 2022-11-19 17:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0004_alter_eventquestionstate_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="location",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
