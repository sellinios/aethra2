from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Peloponnese region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Peloponnese", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Argos-Mykines", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Argos", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Corinth", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of East Mani", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Epidaurus", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Ermionida", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Evrotas", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Gortynia", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Kalamata", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Megalopolis", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Messini", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Monemvasia", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Nafplion", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Nemea", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of North Kynouria", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Oichalia", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Pylos-Nestor", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Sikyona", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of South Kynouria", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Sparta", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Trifylia", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Tripoli", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Velo-Vocha", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of West Mani", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
            {"name": "Municipality of Xylokastro-Evrostina", "slug": "", "parent": "peloponnese", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Peloponnese'))