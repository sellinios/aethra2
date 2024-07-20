from rest_framework.decorators import api_view
from rest_framework.response import Response
from geography.models import GeographicPlace, GeographicDivision
from weather.models import GFSForecast
from api.serializers.serializer_weather_city import GFSForecastCitySerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.utils.translation import gettext as _
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def weather_for_city(request, lang_code):
    cities = request.query_params.getlist('cities')
    if not cities:
        return Response({'error': _('No cities provided')}, status=400)

    weather_data = []

    for city_slug in cities:
        try:
            logger.debug(_('Fetching place for slug: {city_slug} and language: {lang_code}').format(city_slug=city_slug, lang_code=lang_code))
            places = GeographicPlace.objects.language(lang_code).filter(translations__slug=city_slug)

            if not places.exists():
                logger.warning(_('No places found for slug: {city_slug}').format(city_slug=city_slug))
                continue

            unique_places = {}
            for place in places:
                key = (place.latitude, place.longitude)
                if key not in unique_places:
                    unique_places[key] = place

            place = list(unique_places.values())[0]
            logger.debug(_('Selected Place: {name} ({latitude}, {longitude})').format(name=place.safe_translation_getter('name', lang_code, 'en'), latitude=place.latitude, longitude=place.longitude))

            user_location = Point(place.longitude, place.latitude, srid=4326)
            forecasts = GFSForecast.objects.annotate(distance=Distance('location', user_location)).order_by(
                'distance').filter(distance__lte=100000)

            if not forecasts.exists():
                logger.debug(_('No forecasts found for place: {place}').format(place=place.safe_translation_getter('name', lang_code, 'en')))
                continue

            serializer = GFSForecastCitySerializer(forecasts, many=True)
            weather_data.append({
                'city': place.safe_translation_getter('name', lang_code, 'en'),
                'forecasts': serializer.data
            })

        except Exception as e:
            logger.error(_('Error fetching weather data for city {city_slug}: {error}').format(city_slug=city_slug, error=str(e)), exc_info=True)
            return Response({'error': str(e)}, status=500)

    return Response(weather_data)