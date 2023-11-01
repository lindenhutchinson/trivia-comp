from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Add any additional fields or customizations you need for your user model.

    # Define related names for groups and user permissions to avoid clashes.
    groups = models.ManyToManyField("auth.Group", related_name="custom_users")
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_users"
    )


class Competition(models.Model):
    code = models.CharField(unique=True, max_length=16)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True, default=None)
    started_at = models.DateTimeField(null=True, blank=True, default=None)
    end_time = models.DateTimeField(null=True, blank=True, default=None)
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    
    trivia_set = models.ManyToManyField("Trivia", through="CompetitionTrivia")

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    # Add additional fields to track participant progress if needed.

    def __str__(self):
        return f"{self.user.username} in {self.competition.name}"


class TriviaCategory(models.Model):
    # taken from the trivia API
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return self.name


class Trivia(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    class QuestionTypes(models.TextChoices):
        BOOL = "boolean", "True / False"
        MULTIPLE = "multiple", "Multiple Choice"

    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    question_type = models.CharField(max_length=10, choices=QuestionTypes.choices)
    question = models.TextField(unique=True)
    answer = models.TextField()
    incorrect_answers = models.JSONField()
    category = models.ForeignKey(TriviaCategory, on_delete=models.CASCADE)
    # Add other fields as needed.

    def __str__(self):
        return self.question


class CompetitionTrivia(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['competition', 'trivia'],
                name='unique_competition_trivia'
            )
        ]


class SeenCompetitionTrivia(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    trivia = models.ForeignKey(Trivia, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['competition', 'trivia'],
                name='unique_seen_competition_trivia'
            )
        ]