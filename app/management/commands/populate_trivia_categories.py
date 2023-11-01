import requests
from django.core.management.base import BaseCommand
from app.models import TriviaCategory

class Command(BaseCommand):
    help = 'Populate TriviaCategory table with data from the OpenTDB API'

    def handle(self, *args, **options):
        if TriviaCategory.objects.exists():
            self.stdout.write(self.style.SUCCESS('TriviaCategory table is not empty. Skipping data population.'))
            return

        # API URL for trivia categories
        api_url = 'https://opentdb.com/api_category.php'

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if 'trivia_categories' in data:
                for category_data in data['trivia_categories']:
                    TriviaCategory.objects.create(
                        id=category_data['id'],
                        name=category_data['name']
                    )
                self.stdout.write(self.style.SUCCESS('TriviaCategory table populated successfully.'))
            else:
                self.stderr.write(self.style.ERROR('No trivia categories found in the API response.'))
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error fetching data from the API: {str(e)}'))