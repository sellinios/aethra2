from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run import commands for all 13 regions'

    def handle(self, *args, **options):
        commands = [
            'import_attica',
            'import_central_greece',
            'import_central_macedonia',
            'import_crete',
            'import_eastern_macedonia_and_thrace',
            'import_epirus',
            'import_ionian_islands',
            'import_north_aegean',
            'import_peloponnese',
            'import_south_aegean',
            'import_thessaly',
            'import_western_greece',
            'import_western_macedonia'
        ]

        for command in commands:
            try:
                self.stdout.write(self.style.NOTICE(f'Running command: {command}'))
                call_command(command)
                self.stdout.write(self.style.SUCCESS(f'Successfully ran command: {command}'))
            except CommandError as e:
                self.stdout.write(self.style.ERROR(f'Error running command {command}: {e}'))

        self.stdout.write(self.style.SUCCESS('Completed importing all regions'))