# Generated by Django 4.2a1 on 2023-03-02 17:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EventQuestionState",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("question_number", models.IntegerField()),
                ("round_number", models.IntegerField()),
                ("question_displayed", models.BooleanField(default=False)),
                ("answer_displayed", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["event", "round_number", "question_number"],
            },
        ),
        migrations.CreateModel(
            name="EventRoundState",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("round_number", models.IntegerField()),
                ("locked", models.BooleanField(default=False)),
                ("scored", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["event", "round_number"],
            },
        ),
        migrations.CreateModel(
            name="Game",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("block_code", models.CharField(default="", max_length=150)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, null=True)),
                ("date_used", models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                "ordering": ["-date_used", "title"],
            },
        ),
        migrations.CreateModel(
            name="GameQuestion",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("round_number", models.IntegerField()),
                ("question_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="GameRound",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("title", models.CharField(max_length=128)),
                ("round_description", models.TextField(blank=True, default="")),
                ("round_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Leaderboard",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("public_through_round", models.IntegerField(blank=True, null=True)),
                ("host_through_round", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="LeaderboardEntry",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "leaderboard_type",
                    models.IntegerField(choices=[(0, "Host"), (1, "Public")]),
                ),
                ("rank", models.IntegerField(blank=True, null=True)),
                ("tiebreaker_rank", models.IntegerField(blank=True, null=True)),
                ("total_points", models.FloatField(default=0)),
            ],
            options={
                "verbose_name_plural": "Leaderboard Entries",
                "ordering": ["event", "rank", "tiebreaker_rank", "pk"],
            },
        ),
        migrations.CreateModel(
            name="Location",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=128)),
                ("address", models.TextField(blank=True, null=True)),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Question",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "question_type",
                    models.IntegerField(
                        choices=[
                            (0, "General Knowledge"),
                            (1, "Themed Round"),
                            (2, "Word Play"),
                            (3, "Image Round"),
                            (4, "Lightning Round"),
                            (5, "Sound Round"),
                            (6, "Tiebreaker"),
                        ],
                        default=0,
                    ),
                ),
                ("question_text", models.TextField()),
                (
                    "question_url",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "answer_notes",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionAnswer",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("text", models.CharField(db_index=True, max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="QuestionResponse",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("recorded_answer", models.TextField(default="")),
                ("fuzz_ratio", models.IntegerField(default=0)),
                ("points_awarded", models.FloatField(default=0)),
                ("funny", models.BooleanField(default=False)),
                ("locked", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=200)),
                ("password", models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="TiebreakerQuestion",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="TriviaEvent",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "joincode",
                    models.CharField(db_index=True, max_length=64, unique=True),
                ),
                ("current_round_number", models.IntegerField(default=1)),
                ("current_question_number", models.IntegerField(default=1)),
                ("player_limit", models.IntegerField(blank=True, null=True)),
                (
                    "event_teams",
                    models.ManyToManyField(
                        blank=True, related_name="event_teams", to="game.team"
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="game.game"
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="game.location",
                    ),
                ),
            ],
        ),
    ]
