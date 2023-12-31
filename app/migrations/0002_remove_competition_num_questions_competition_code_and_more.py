# Generated by Django 4.2.1 on 2023-10-31 08:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="competition",
            name="num_questions",
        ),
        migrations.AddField(
            model_name="competition",
            name="code",
            field=models.CharField(
                default=datetime.datetime(
                    2023, 10, 31, 8, 46, 38, 101031, tzinfo=datetime.timezone.utc
                ),
                max_length=16,
                unique=True,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="competition",
            name="questions",
            field=models.ManyToManyField(to="app.trivia"),
        ),
        migrations.AddField(
            model_name="trivia",
            name="question_type",
            field=models.CharField(
                choices=[("bool", "True / False"), ("multiple", "Multiple Choice")],
                default="bool",
                max_length=10,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="trivia",
            name="difficulty",
            field=models.CharField(
                choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="CompetitionTrivia",
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
                (
                    "competition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.competition",
                    ),
                ),
                (
                    "trivia",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.trivia"
                    ),
                ),
            ],
        ),
    ]
