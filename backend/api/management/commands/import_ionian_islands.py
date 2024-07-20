from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Ionian Islands region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Ionian Islands", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Argostoli", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
            {"name": "Municipality of Central Corfu and Diapontian Islands", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
            {"name": "Municipality of Lefkada", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
            {"name": "Municipality of Lixouri", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
            {"name": "Municipality of Meganisi", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
            {"name": "Municipality of North Corfu", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
            {"name": "Municipality of Paxos", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
            {"name": "Municipality of Sami", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
            {"name": "Municipality of South Corfu", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
            {"name": "Municipality of Zakynthos", "slug": "", "parent": "ionian-islands", "level_name": "Municipality"},
        ]

        # Import divisions
        for item in divisions:
            name = item['name']
            slug = item['slug'] or slugify(name)
            parent_slug = item['parent']
            level_name = item['level_name']

            parent = None
            if parent_slug:
                try:
                    parent = GeographicDivision.objects.get(slug=parent_slug)
                except GeographicDivision.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Parent division with slug "{parent_slug}" does not exist.'))
                    continue

            # Check if the division already exists
            division, created = GeographicDivision.objects.get_or_create(
                name=name,
                slug=slug,
                parent=parent,
                level_name=level_name
            )

            # If the division was just created, it will have an ID assigned automatically
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created division: {name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Division already exists: {name}'))

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Ionian Islands'))