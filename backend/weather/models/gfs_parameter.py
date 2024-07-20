from django.db import models
from django.utils import timezone

class GFSParameter(models.Model):
    """Model to store GFS parameter information."""
    number = models.IntegerField(unique=True)
    level_layer = models.CharField(max_length=255)
    parameter = models.CharField(max_length=255)
    forecast_valid = models.CharField(max_length=255, default="N/A")
    description = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('number', 'level_layer', 'parameter')

    def __str__(self):
        return f"{self.parameter} (ID: {self.number}, Level: {self.level_layer}, Forecast Valid: {self.forecast_valid})"