from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Crete region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Crete", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Agios Nikolaos", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Agios Vasileios", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Amari", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Anogeia", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Apokoronas", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Archanes-Asterousia", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Faistos", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Gavdos", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Gortyn", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Heraklion", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Hersonissos", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Ierapetra", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Kantanos-Selino", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Kissamos", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Lasithi Plateau", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Malevizi", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Minoa Pediada", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Mylopotamos", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Platanias", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Rethymno", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Sfakia", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Sitia", "slug": "", "parent": "crete", "level_name": "Municipality"},
            {"name": "Municipality of Viannos", "slug": "", "parent": "crete", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Crete'))