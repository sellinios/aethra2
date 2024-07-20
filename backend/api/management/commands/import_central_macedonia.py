from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Central Macedonia region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Central Macedonia", "slug": "central-macedonia", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Alexandreia", "slug": "alexandreia", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Almopia", "slug": "almopia", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Ampelokipoi-Menemeni", "slug": "ampelokipoi-menemeni", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Amphipolis", "slug": "amphipolis", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Aristotelis", "slug": "aristotelis", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Chalkidona", "slug": "chalkidona", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Delta", "slug": "delta", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Dion-Olympos", "slug": "dion-olympos", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Edessa", "slug": "edessa", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Emmanouil Pappas", "slug": "emmanouil-pappas", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Irakleia", "slug": "irakleia", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Kalamaria", "slug": "kalamaria", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Kassandra", "slug": "kassandra", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Katerini", "slug": "katerini", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Kilkis", "slug": "kilkis", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Kordelio-Evosmos", "slug": "kordelio-evosmos", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Lagkadas", "slug": "lagkadas", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Naousa", "slug": "naousa", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Nea Propontida", "slug": "nea-propontida", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Nea Zichni", "slug": "nea-zichni", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Neapoli-Sykies", "slug": "neapoli-sykies", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Oraiokastro", "slug": "oraiokastro", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Paionia", "slug": "paionia", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Pavlos Melas", "slug": "pavlos-melas", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Pella", "slug": "pella", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Polygyros", "slug": "polygyros", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Pydna-Kolindros", "slug": "pydna-kolindros", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Pylaia-Chortiatis", "slug": "pylaia-chortiatis", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Sintiki", "slug": "sintiki", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Sithonia", "slug": "sithonia", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Skydra", "slug": "skydra", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Thermaikos", "slug": "thermaikos", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Thermi", "slug": "thermi", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Veria", "slug": "veria", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Visaltia", "slug": "visaltia", "parent": "central-macedonia", "level_name": "Municipality"},
            {"name": "Municipality of Volvi", "slug": "volvi", "parent": "central-macedonia", "level_name": "Municipality"}
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Central Macedonia'))