# Generated by Django 4.0.5 on 2022-06-22 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_team_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
