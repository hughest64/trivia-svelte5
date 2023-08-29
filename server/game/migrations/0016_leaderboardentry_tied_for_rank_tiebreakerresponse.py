# Generated by Django 4.2.2 on 2023-07-25 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0015_alter_leaderboardentry_points_adjustment"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaderboardentry",
            name="tied_for_rank",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="TiebreakerResponse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("recorded_answer", models.IntegerField()),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tiebreaker_responses",
                        to="game.triviaevent",
                    ),
                ),
                (
                    "leaderboard_entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="game.leaderboardentry",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tiebreaker_responses",
                        to="game.team",
                    ),
                ),
                (
                    "tiebreaker_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="game.tiebreakerquestion",
                    ),
                ),
            ],
        ),
    ]