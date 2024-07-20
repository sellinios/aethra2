from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Western Macedonia region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Western Macedonia", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Amyntaio", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Argos Orestiko", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Deskati", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Eordaia", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Florina", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Grevena", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Kozani", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Nestorio", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Prespes", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Servia", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Velventos", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Voio", "slug": "", "parent": "western-macedonia", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Western Macedonia'))