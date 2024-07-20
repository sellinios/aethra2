# api/serializers/serializer_weather_mountains.py
from rest_framework import serializers
import math

class GFSForecastMountainsSerializer(serializers.Serializer):
    date = serializers.DateField()
    hour = serializers.IntegerField()
    temperature_celsius = serializers.SerializerMethodField()
    wind_speed = serializers.SerializerMethodField()
    wind_direction = serializers.SerializerMethodField()
    precipitation_rate = serializers.SerializerMethodField()

    def get_temperature_celsius(self, obj):
        return obj['forecast_data']['temperature_level_2_heightAboveGround']

    def get_wind_speed(self, obj):
        u = obj['forecast_data'].get('u-component_of_wind_level_10_heightAboveGround')
        v = obj['forecast_data'].get('v-component_of_wind_level_10_heightAboveGround')
        if u is not None and v is not None:
            return math.sqrt(u**2 + v**2)
        return None

    def get_wind_direction(self, obj):
        u = obj['forecast_data'].get('u-component_of_wind_level_10_heightAboveGround')
        v = obj['forecast_data'].get('v-component_of_wind_level_10_heightAboveGround')
        if u is not None and v is not None:
            direction = (math.atan2(v, u) * 180 / math.pi + 360) % 360
            return direction
        return None

    def get_precipitation_rate(self, obj):
        return obj['forecast_data'].get('precipitation_rate_surface')