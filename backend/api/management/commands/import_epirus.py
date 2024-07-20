from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Epirus region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Epirus", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Arta", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Central Tzoumerka", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Dodoni", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Filiates", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Georgios Karaiskakis", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Igoumenitsa", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Ioannina", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Konitsa", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Metsovo", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Nikolaos Skoufas", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of North Tzoumerka", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Parga", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Pogoni", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Preveza", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Souli", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Zagori", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Ziros", "slug": "", "parent": "epirus", "level_name": "Municipality"},
            {"name": "Municipality of Zitsa", "slug": "", "parent": "epirus", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Epirus'))