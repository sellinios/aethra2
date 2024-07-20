from django.core.management.base import BaseCommand
from django.utils.text import slugify
from geography.models import GeographicDivision, GeographicCategory  # Adjust these imports based on your app name
from unidecode import unidecode  # Import unidecode


class Command(BaseCommand):
    help = 'Import Attica region and municipalities data'

    def handle(self, *args, **options):
        divisions = [
            {"name": "Attica", "slug": "", "parent": None, "level_name": "Region"},
            {"name": "Municipality of Acharnes", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Aegina", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Agia Paraskevi", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Agia Varvara", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Agioi Anargyroi-Kamatero", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Agios Dimitrios", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Agistri", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Aigaleo", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Alimos", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Aspropyrgos", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Chalandri", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Dafni-Ymittos", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Dionysos", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Elefsina", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Elliniko-Argyroupoli", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Filothei-Psychiko", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Fyli", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Galatsi", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Glyfada", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Haidari", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Hydra", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Ilion", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Ilioupoli", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Irakleio", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Kaisariani", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Kallithea", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Keratsini-Drapetsona", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Kifissia", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Korydallos", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Kropia", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Kythira", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Lavreotiki", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Lykovrysi-Pefki", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Mandra-Eidyllia", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Markopoulo Mesogaias", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Marousi", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Megara", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Metamorfosi", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Moschato-Tavros", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Nea Filadelfeia-Nea Chalkidona", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Nea Ionia", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Nea Smyrni", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Nikaia-Agios Ioannis Rentis", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Oropos", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Paiania", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Palaio Faliro", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Pallini", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Papagou-Cholargos", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Penteli", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Perama", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Peristeri", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Petroupoli", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Piraeus", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Rafina-Pikermi", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Salamis Island", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Saronikos", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Spata-Artemida", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Spetses", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Troizinia-Methana", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Vari-Voula-Vouliagmeni", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Vrilissia", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Vyronas", "slug": "", "parent": "attica", "level_name": "Municipality"},
            {"name": "Municipality of Zografou", "slug": "", "parent": "attica", "level_name": "Municipality"},
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

        self.stdout.write(self.style.SUCCESS('Completed importing municipalities for Attica'))