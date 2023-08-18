# Generated by Django 4.2.2 on 2023-08-16 12:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0020_alter_tiebreakerresponse_recorded_answer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="name",
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name="team",
            name="password",
            field=models.CharField(db_index=True, max_length=120, unique=True),
        ),
    ]
