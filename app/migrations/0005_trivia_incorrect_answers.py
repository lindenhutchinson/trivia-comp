# Generated by Django 4.2.1 on 2023-10-31 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_alter_trivia_id_alter_trivia_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="trivia",
            name="incorrect_answers",
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
    ]