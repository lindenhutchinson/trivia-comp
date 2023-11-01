import requests
import random
import string
from .models import SeenCompetitionTrivia, Trivia, TriviaCategory, CompetitionTrivia
import html
from django.forms.models import model_to_dict
import json

def generate_random_string(length):
    """Generate a random string up to the given maximum length."""
    valid_chars = [
        c for c in string.ascii_letters if c not in ["l", "I", "i", "O", "o"]
    ]
    return "".join(random.choice(valid_chars) for _ in range(length))


def save_trivia_data_from_api(api_data, competition):
    trivia_list = []
    for question_data in api_data:
        # Extract relevant data from the API response
        question = html.unescape(question_data["question"])
        answer = html.unescape(question_data["correct_answer"])
        incorrect_answers = json.dumps([html.unescape(q) for q in question_data["incorrect_answers"]])
        difficulty = question_data["difficulty"]
        question_type = question_data["type"]
        category_name = question_data["category"]

        # Retrieve or create the associated TriviaCategory
        category, _ = TriviaCategory.objects.get_or_create(name=category_name)

        # Create a new Trivia object
        trivia, _ = Trivia.objects.get_or_create(
            question=question,
            answer=answer,
            incorrect_answers=incorrect_answers,
            difficulty=difficulty,
            question_type=question_type,
            category=category,
        )

        _, comp_trivia_created = CompetitionTrivia.objects.get_or_create(
            competition=competition,
            trivia=trivia
        )
        

        if comp_trivia_created:
            SeenCompetitionTrivia.objects.create(
                competition=competition,
                trivia=trivia
            )
            
            # dont duplicate questions that already exist on the page
            trivia_list.append({
                **model_to_dict(trivia),
                'category_name':trivia.category.name
            })
        
    return trivia_list

