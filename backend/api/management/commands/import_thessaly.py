from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Thessaly region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Thessaly", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Agia", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Almyros", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Alonnisos", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Argithea", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Elassona", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Farkadona", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Farsala", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Karditsa", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Kileler", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Lake Plastiras", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Larissa", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Meteora", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Mouzaki", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Palamas", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Pyli", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Rigas Feraios", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Skiathos", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Sofades", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of South Pelion", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Tempi", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Trikala", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Tyrnavos", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Volos", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
            {"name": "Municipality of Zagora-Mouresi", "slug": "", "parent": "thessaly", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Thessaly'))