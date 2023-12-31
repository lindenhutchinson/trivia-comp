# Generated by Django 4.2.1 on 2023-10-31 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_remove_competition_num_questions_competition_code_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="competition",
            name="questions",
        ),
        migrations.AddField(
            model_name="competition",
            name="trivia_set",
            field=models.ManyToManyField(
                through="app.CompetitionTrivia", to="app.trivia"
            ),
        ),
    ]
