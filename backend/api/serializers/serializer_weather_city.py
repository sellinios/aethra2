from rest_framework import serializers
from weather.models import GFSForecast
import math


class GFSForecastCitySerializer(serializers.ModelSerializer):
    temperature_celsius = serializers.SerializerMethodField()
    wind_speed = serializers.SerializerMethodField()
    wind_direction = serializers.SerializerMethodField()

    class Meta:
        model = GFSForecast
        fields = ['date', 'hour', 'temperature_celsius', 'wind_speed', 'wind_direction', 'forecast_data']

    def get_temperature_celsius(self, obj):
        temperature_kelvin = obj.forecast_data.get("temperature_level_2_heightAboveGround")
        if temperature_kelvin is not None:
            return round(temperature_kelvin - 273.15, 2)
        return None

    def get_wind_speed(self, obj):
        u = obj.forecast_data.get("u-component_of_wind_level_10_heightAboveGround")
        v = obj.forecast_data.get("v-component_of_wind_level_10_heightAboveGround")
        if u is not None and v is not None:
            return round(math.sqrt(u ** 2 + v ** 2), 2)
        return None

    def get_wind_direction(self, obj):
        u = obj.forecast_data.get("u-component_of_wind_level_10_heightAboveGround")
        v = obj.forecast_data.get("v-component_of_wind_level_10_heightAboveGround")
        if u is not None and v is not None:
            direction = (math.atan2(v, u) * 180 / math.pi + 360) % 360
            return round(direction, 2)
        return None
