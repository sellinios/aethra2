from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Central Greece region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Central Greece", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Agrafa", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Aliartos-Thespies", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Amfikleia-Elateia", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Chalcis", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Delphi", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Dirfys-Messapia", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Distomo-Arachova-Antikyra", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Domokos", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Dorida", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Eretria", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Istiaia-Aidipsos", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Kamena Vourla", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Karpenisi", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Karystos", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Kymi-Aliveri", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Livadeia", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Lokroi", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Makrakomi", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Mantoudi-Limni-Agia Anna", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Orchomenus", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Skyros", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Stylida", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Tanagra", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
            {"name": "Municipality of Thebes", "slug": "", "parent": "central-greece", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Central Greece'))