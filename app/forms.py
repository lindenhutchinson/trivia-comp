# forms.py
from django import forms

from .models import CompetitionTrivia, User, Competition, TriviaCategory, Trivia


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class CompetitionForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Competition
        fields = ["name"]


class JoinCompetitionForm(forms.Form):
    name = forms.CharField(max_length=16)



class TriviaQuestionForm(forms.Form):
    NUM_CHOICES = [(i, i) for i in range(1, 11)]  # Limit to fetching up to 10 questions
    CATEGORY_CHOICES = [
        (category.id, category.name) for category in TriviaCategory.objects.all()
    ]
    CATEGORY_CHOICES.insert(0, ('any', "Any"))

    num_questions = forms.ChoiceField(
        choices=NUM_CHOICES,
        label="Number of Questions",
        initial=5,  # Set an initial value
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label="Category",
        initial='any',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    QUESTION_TYPE_CHOICES = [
        ("any", "Any"),
        ("multiple", "Multiple Choice"),
        ("boolean", "True/False"),
    ]
    question_type = forms.ChoiceField(
        choices=QUESTION_TYPE_CHOICES,
        label="Question Type",
        initial='any',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    DIFFICULTY_CHOICES = [
        ("any", "Any"),
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        label="Difficulty",
        initial='any',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class DateInput(forms.DateInput):
    input_type = 'datetime'

class CompetitionSettingsForm(forms.Form):
    end_time = forms.DateTimeField(
        label="End Time",
        widget=DateInput(attrs={"class": "form-control"}),
        required=False,
        input_formats=['%Y-%m-%d %H:%M:%S'],
    )
    start_competition = forms.BooleanField(
        label="Start Competition",
        required=False,
        initial=True
    )