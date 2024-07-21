from django.contrib.gis.db import models as gis_models


class GeographicData(gis_models.Model):
    gid = gis_models.CharField(max_length=50, unique=True)
    name = gis_models.CharField(max_length=255)
    geometry = gis_models.MultiPolygonField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
