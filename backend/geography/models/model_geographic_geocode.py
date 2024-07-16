# model_geographic_geocode.py
from django.db import models
from .model_geographic_place import GeographicPlace

class GeocodeResult(models.Model):
    geographic_place = models.OneToOneField(GeographicPlace, on_delete=models.CASCADE, related_name='geocode')
    geocode_result = models.JSONField(null=True, blank=True)
    geocode_last_updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Geocode Result"
        verbose_name_plural = "Geocode Results"

    def __str__(self):
        return f"Geocode Result for {self.geographic_place}"