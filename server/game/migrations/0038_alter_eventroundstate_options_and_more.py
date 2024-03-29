# Generated by Django 4.2.10 on 2024-02-29 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0037_alter_tiebreakerresponse_recorded_answer"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eventroundstate",
            options={"ordering": ["-event", "round_number"]},
        ),
        migrations.AlterModelOptions(
            name="gamequestion",
            options={"ordering": ["game", "round_number", "question_number"]},
        ),
        migrations.AlterModelOptions(
            name="location",
            options={"ordering": ["-active", "name"]},
        ),
        migrations.AlterField(
            model_name="leaderboard",
            name="event",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leaderboard",
                to="game.triviaevent",
            ),
        ),
    ]
