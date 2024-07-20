# api/serializers/serializer_gfs_forecast.py
from rest_framework import serializers
from weather.models import GFSForecast

class GFSForecastSerializer(serializers.ModelSerializer):
    precipitation = serializers.SerializerMethodField()

    class Meta:
        model = GFSForecast
        fields = ['latitude', 'longitude', 'precipitation']

    def get_precipitation(self, obj):
        return obj.forecast_data.get('total_precipitation_level_0_surface', 0)