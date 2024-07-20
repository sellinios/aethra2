from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Eastern Macedonia and Thrace region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Eastern Macedonia and Thrace", "slug": "eastern-macedonia-and-thrace", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Abdera", "slug": "abdera", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Alexandroupolis", "slug": "alexandroupolis", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Arriana", "slug": "arriana", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Didymoteicho", "slug": "didymoteicho", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Doxato", "slug": "doxato", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Drama", "slug": "drama", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Iasmos", "slug": "iasmos", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Kato Nevrokopi", "slug": "kato-nevrokopi", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Kavala", "slug": "kavala", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Komotini", "slug": "komotini", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Maroneia-Sapes", "slug": "maroneia-sapes", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Myki", "slug": "myki", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Nestos", "slug": "nestos", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Pangaio", "slug": "pangaio", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Paranesti", "slug": "paranesti", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Prosotsani", "slug": "prosotsani", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Samothrace", "slug": "samothrace", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Soufli", "slug": "soufli", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Thasos", "slug": "thasos", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Topeiros", "slug": "topeiros", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
            {"name": "Municipality of Xanthi", "slug": "xanthi", "parent": "eastern-macedonia-and-thrace", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Eastern Macedonia and Thrace'))