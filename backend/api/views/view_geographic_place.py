import logging
import googlemaps
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geography.models import GeographicPlace, GeographicCategory, GeographicDivision
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from unidecode import unidecode
from django.utils.text import slugify

logger = logging.getLogger(__name__)

# Initialize the Google Maps client with your API key
# gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

@api_view(['GET'])
def nearest_place(request, lang_code):
    try:
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        logger.debug(f"Received request for nearest place: latitude={latitude}, longitude={longitude}")

        if not latitude or not longitude:
            logger.error("Latitude and longitude are required")
            return Response({"error": "Latitude and longitude are required"}, status=400)

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            logger.error("Invalid latitude or longitude format")
            return Response({"error": "Invalid latitude or longitude format"}, status=400)

        user_location = Point(longitude, latitude, srid=4326)

        # Find the nearest place within 100 meters
        nearest_place = GeographicPlace.objects.annotate(distance=Distance('location', user_location)).filter(
            distance__lte=0.1).order_by('distance').first()
        logger.debug(f"Nearest place found: {nearest_place}")

        if nearest_place:
            if not nearest_place.confirmed:
                logger.debug(f"Nearest place at ({nearest_place.latitude}, {nearest_place.longitude}) is not confirmed, querying Google Places API")
                places_result = gmaps.places_nearby(location=(nearest_place.latitude, nearest_place.longitude),
                                                    rank_by='distance', keyword='point of interest')
                logger.debug(f"Google Places API response: {places_result}")

                if places_result['results']:
                    for google_place in places_result['results']:
                        place_details = gmaps.place(place_id=google_place['place_id'])
                        logger.debug(f"Place details from Google Places API: {place_details}")

                        if 'result' in place_details and 'name' in place_details['result']:
                            place_name = place_details['result']['name']
                            nearest_place.set_current_language('en')
                            nearest_place.name = place_name
                            nearest_place.slug = slugify(unidecode(place_name))
                            nearest_place.confirmed = True  # Mark as confirmed
                            nearest_place.save()
                            logger.debug(f"Nearest place updated with name: {place_name} and marked as confirmed")
                            break
                        else:
                            logger.debug("Google Places API did not return a valid place name")
                else:
                    logger.debug("No results found from Google Places API")
            else:
                logger.debug(f"Nearest place is already confirmed: {nearest_place.safe_translation_getter('name', lang_code, 'en')}")

        else:
            logger.debug(f"No place found within 100 meters, querying Google Places API for a new place")
            places_result = gmaps.places_nearby(location=(latitude, longitude), rank_by='distance',
                                                keyword='point of interest')
            logger.debug(f"Google Places API response: {places_result}")

            if places_result['results']:
                for google_place in places_result['results']:
                    place_details = gmaps.place(place_id=google_place['place_id'])
                    logger.debug(f"Place details from Google Places API: {place_details}")

                    if 'result' in place_details and 'name' in place_details['result']:
                        place_name = place_details['result']['name']

                        # Get or create the default category and admin division
                        default_category, created = GeographicCategory.objects.get_or_create(
                            slug=slugify(unidecode('Default')),
                            defaults={'name': 'Default'}
                        )
                        default_division, created = GeographicDivision.objects.get_or_create(
                            slug=slugify(unidecode('Default')),
                            defaults={'name': 'Default', 'level_name': 'Division'}
                        )

                        new_place = GeographicPlace(
                            longitude=longitude,
                            latitude=latitude,
                            category=default_category,
                            admin_division=default_division,
                            location=Point(longitude, latitude, srid=4326)
                        )
                        new_place.name = place_name
                        new_place.slug = slugify(unidecode(place_name))
                        new_place.confirmed = True  # Mark as confirmed
                        new_place.save()
                        logger.debug(f"Created new place with name: {place_name}")
                        nearest_place = new_place
                        break
                    else:
                        logger.debug("Google Places API did not return a valid place name")
                        return Response({"error": "Google Places API did not return a valid place name"}, status=500)
            else:
                logger.debug("No results found from Google Places API")
                return Response({"error": "No results found from Google Places API"}, status=404)

        data = {
            "name": nearest_place.safe_translation_getter('name', lang_code, 'en'),
            "slug": nearest_place.slug,
            "latitude": nearest_place.latitude,
            "longitude": nearest_place.longitude,
            "admin_division": {
                "slug": nearest_place.admin_division.slug,
                "parent": {
                    "slug": nearest_place.admin_division.parent.slug,
                    "parent": {
                        "slug": nearest_place.admin_division.parent.parent.slug,
                        "parent": {
                            "slug": nearest_place.admin_division.parent.parent.parent.slug,
                        } if nearest_place.admin_division.parent.parent.parent else None
                    } if nearest_place.admin_division.parent.parent else None
                } if nearest_place.admin_division.parent else None
            } if nearest_place.admin_division else None
        }
        return Response(data)
    except Exception as e:
        logger.error(f"Error in nearest_place view: {str(e)}")
        return Response({"error": str(e)}, status=500)