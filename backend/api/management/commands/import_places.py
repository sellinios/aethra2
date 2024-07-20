import time
from multiprocessing import Pool
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from geography.models import GeographicPlace, GeographicCategory, GeographicDivision
from unidecode import unidecode
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Import geographic places for Greece at every 10 meters interval'

    def handle(self, *args, **options):
        start_time = time.time()

        # Zero the counters by clearing the table
        GeographicPlace.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared all existing geographic places.'))

        # Define the bounding box for Greece
        min_lat, max_lat = 34.802066, 41.748878
        min_lng, max_lng = 19.316406, 28.256348
        interval = 0.001

        # Default category
        default_category, created = GeographicCategory.objects.get_or_create(
            slug=slugify(unidecode('Default')),
            defaults={'name': 'Default'}
        )

        # Default admin division
        default_division, created = GeographicDivision.objects.get_or_create(
            slug=slugify(unidecode('Default')),
            defaults={'name': 'Default', 'level_name': 'Division'}
        )

        lat_steps = list(frange(min_lat, max_lat, interval))
        lng_steps = list(frange(min_lng, max_lng, interval))
        total_steps = len(lat_steps) * len(lng_steps)

        self.stdout.write(f'Total lat steps: {len(lat_steps)}, Total lng steps: {len(lng_steps)}')
        self.stdout.write(f'Total places to insert: {total_steps}')

        # Divide the task into chunks for parallel processing
        chunk_size = 100000  # Adjust based on memory and performance
        lat_chunks = [lat_steps[i:i + chunk_size] for i in range(0, len(lat_steps), chunk_size)]

        with Pool() as pool:
            results = pool.starmap(process_chunk, [(chunk, lng_steps, default_category, default_division) for chunk in lat_chunks])

        end_time = time.time()
        self.stdout.write(self.style.SUCCESS(f'Completed importing geographic places in {end_time - start_time:.2f} seconds.'))

def process_chunk(lat_chunk, lng_steps, default_category, default_division):
    places = []
    for lat in lat_chunk:
        for lng in lng_steps:
            # Round latitude and longitude to six decimal places
            lat = round(lat, 6)
            lng = round(lng, 6)
            place = GeographicPlace(
                longitude=lng,
                latitude=lat,
                category=default_category,
                admin_division=default_division
            )
            places.append(place)
            if len(places) >= 10000:  # Batch insert every 10000 places
                GeographicPlace.objects.bulk_create(places)
                places = []

    if places:
        GeographicPlace.objects.bulk_create(places)

def frange(start, stop, step):
    while start < stop:
        yield round(start, 6)  # Ensure step values are rounded to six decimal places
        start += step