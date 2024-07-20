from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Western Greece region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Western Greece", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Agrinio", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Aigialeia", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Aktio-Vonitsa", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Amfilochia", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Andravida-Kyllini", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Andritsaina-Krestena", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Erymanthos", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Ilida", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Kalavryta", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Missolonghi", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Nafpaktia", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Olympia", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Patras", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Pineios", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Pyrgos", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Thermo", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of West Achaea", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Xiromero", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
            {"name": "Municipality of Zacharo", "slug": "", "parent": "western-greece", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Western Greece'))