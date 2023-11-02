from .models import Trivia, TriviaCategory, CompetitionTrivia, SeenCompetitionTrivia
from django.forms.models import model_to_dict
import html
import json
from .trivia_api import OpenTriviaAPI
import random


class TriviaCache:
    def __init__(self):
        self.api_instance = OpenTriviaAPI()

    def get_trivia(
        self, num_questions, category, difficulty, question_type, competition
    ):
        try:
            num_questions = int(num_questions)
        except TypeError:
            # fuck you, why isnt it an integer?
            # no questions for you
            num_questions = 0

        # Check if trivia for the competition with the specified category, difficulty, and question_type
        # already exists in the database
        existing_trivia = self.get_existing_trivia(
            competition, category, difficulty, question_type
        )
        trivia_count = existing_trivia.count()
        if trivia_count >= num_questions:
            # Use existing trivia from the database
            print(f"Pulled {num_questions} questions from cache")
            print(f"Trivia count is: {trivia_count}")
            trivia_idxs = random.choices(range(0, trivia_count), k=num_questions)
            trivia_data = [existing_trivia[i] for i in trivia_idxs]
            trivia_list = self.save_cached_trivia_for_comp(trivia_data, competition)
        else:
            # this will always be > 0
            required_questions_num = num_questions - existing_trivia.count()
            print(f"Retrieving {required_questions_num} questions from API")
            trivia_list = self.save_cached_trivia_for_comp(existing_trivia, competition)

            # Fetch trivia from the API
            api_data = self.api_instance.fetch_questions(
                required_questions_num, category, difficulty, question_type
            )

            # Save trivia to the database and combine it with any cached trivia
            trivia_list = trivia_list + self.save_trivia_to_database(
                api_data, competition
            )
        return trivia_list

    def get_existing_trivia(self, competition, category, difficulty, question_type):
        trivia_query = Trivia.objects
        if category != "any":
            trivia_query = trivia_query.filter(category=category)
        if difficulty != "any":
            trivia_query = trivia_query.filter(difficulty=difficulty)
        if question_type != "any":
            trivia_query = trivia_query.filter(question_type=question_type)

        return trivia_query.exclude(seencompetitiontrivia__competition=competition)

    def save_trivia_to_database(self, api_data, competition):
        trivia_list = []

        for question_data in api_data:
            # Extract and save trivia data to the database
            trivia = self.save_trivia(question_data)

            # Create CompetitionTrivia and SeenCompetitionTrivia entries
            _, comp_trivia_created = CompetitionTrivia.objects.get_or_create(
                competition=competition, trivia=trivia
            )
            if comp_trivia_created:
                SeenCompetitionTrivia.objects.create(
                    competition=competition, trivia=trivia
                )

                # dont duplicate questions that already exist on the page
                trivia_list.append(
                    {**model_to_dict(trivia), "category_name": trivia.category.name}
                )

        return trivia_list

    def save_cached_trivia_for_comp(self, trivia_objects, competition):
        trivia_list = []
        for trivia in trivia_objects:
            _, comp_trivia_created = CompetitionTrivia.objects.get_or_create(
                competition=competition, trivia=trivia
            )
            if comp_trivia_created:
                SeenCompetitionTrivia.objects.create(
                    competition=competition, trivia=trivia
                )

                trivia_list.append({
                    **model_to_dict(trivia),
                    "category_name": trivia.category.name
                })

        return trivia_list

    def save_trivia(self, question_data):
        # Save trivia data to the database
        question = html.unescape(question_data["question"])
        answer = html.unescape(question_data["correct_answer"])
        incorrect_answers = json.dumps(
            [html.unescape(q) for q in question_data["incorrect_answers"]]
        )
        difficulty = question_data["difficulty"]
        question_type = question_data["type"]
        category_name = question_data["category"]

        category, _ = TriviaCategory.objects.get_or_create(name=category_name)

        trivia, _ = Trivia.objects.get_or_create(
            question=question,
            answer=answer,
            incorrect_answers=incorrect_answers,
            difficulty=difficulty,
            question_type=question_type,
            category=category,
        )
        return trivia
