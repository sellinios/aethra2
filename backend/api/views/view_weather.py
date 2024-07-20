from rest_framework.decorators import api_view
from rest_framework.response import Response
from geography.models import GeographicPlace, GeographicDivision
from weather.models import GFSForecast
from api.serializers.serializer_weather import GFSForecastSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
import traceback

@api_view(['GET'])
def weather_for_place(request, lang_code, continent, country, region, subregion, city):
    try:
        # Fetch the parent division
        admin_division = GeographicDivision.objects.get(slug=subregion)
        print(f"Admin Division: {admin_division.name}")

        # Fetch all places matching the city name under the given admin division
        places = GeographicPlace.objects.language(lang_code).filter(admin_division=admin_division,
                                                                    translations__slug=city)

        if not places.exists():
            return Response({'error': 'GeographicPlace does not exist.'}, status=404)

        # Deduplicate by name and coordinates
        unique_places = {}
        for place in places:
            key = (place.latitude, place.longitude)
            if key not in unique_places:
                unique_places[key] = place

        place = list(unique_places.values())[0]
        print(f"Selected Place: {place.safe_translation_getter('name', lang_code, 'en')} ({place.latitude}, {place.longitude})")

        # Calculate the Point location
        user_location = Point(place.longitude, place.latitude, srid=4326)

        # Fetch forecasts near the place
        forecasts = GFSForecast.objects.annotate(distance=Distance('location', user_location)).order_by(
            'distance').filter(distance__lte=100000)  # 100 km radius

        if not forecasts.exists():
            return Response({'error': 'No weather data available for this location.'}, status=404)

        # Adjust the temperature for elevation
        adjusted_forecasts = []
        for forecast in forecasts:
            forecast_data = forecast.forecast_data.copy()
            temperature_kelvin = forecast_data.get("temperature_level_2_heightAboveGround")
            if temperature_kelvin is not None:
                temperature_celsius = temperature_kelvin - 273.15
                # Adjust temperature for elevation
                elevation_adjustment = place.elevation * 0.006
                adjusted_temperature_celsius = temperature_celsius - elevation_adjustment
                forecast_data["temperature_level_2_heightAboveGround"] = adjusted_temperature_celsius + 273.15  # Convert back to Kelvin
            forecast.forecast_data = forecast_data
            adjusted_forecasts.append(forecast)

        serializer = GFSForecastSerializer(adjusted_forecasts, many=True)

        # Debug: Check if the translations are correct
        place_name = place.safe_translation_getter('name', lang_code, 'en')
        place_category = place.category.safe_translation_getter('name', lang_code, 'en')
        print(f"Place Name in {lang_code}: {place_name}")
        print(f"Category Name in {lang_code}: {place_category}")

        return Response({
            'place': place_name,
            'category': place_category,  # Include the category name
            'forecasts': serializer.data
        })

    except GeographicDivision.DoesNotExist:
        return Response({'error': 'GeographicDivision does not exist.'}, status=404)
    except Exception as e:
        print(traceback.format_exc())
        return Response({'error': str(e)}, status=500)