# Generated by Django 4.2.5 on 2023-09-11 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0028_alter_chatmessage_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatmessage",
            name="team",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="chats",
                to="game.team",
            ),
        ),
    ]
