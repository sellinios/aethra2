from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

class GeographicDivision(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    level_name = models.CharField(max_length=255)
    name_variations = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    geographic_data = models.ForeignKey('GeographicData', null=True, blank=True, on_delete=models.SET_NULL, related_name='divisions')
    confirmed = models.BooleanField(default=False)  # Added confirmed field

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'parent', 'level_name')
        verbose_name_plural = "Geographic Divisions"