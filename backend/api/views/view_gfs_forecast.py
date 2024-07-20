# api/views/view_gfs_forecast.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from weather.models import GFSForecast
from django.db.models import Max


@api_view(['GET'])
def gfs_data(request):
    try:
        latest_forecast = GFSForecast.objects.aggregate(latest_cycle=Max('utc_cycle_time'), latest_hour=Max('hour'))
        latest_cycle = latest_forecast['latest_cycle']
        latest_hour = latest_forecast['latest_hour']

        forecasts = GFSForecast.objects.filter(utc_cycle_time=latest_cycle, hour=latest_hour).values(
            'latitude', 'longitude', 'forecast_data', 'hour'
        )

        data = [
            {
                'latitude': forecast['latitude'],
                'longitude': forecast['longitude'],
                'temperature': forecast['forecast_data'].get('temperature_level_2_heightAboveGround'),
                'hour': forecast['hour']
            }
            for forecast in forecasts
        ]

        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)