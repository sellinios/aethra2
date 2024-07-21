# model_geographic_place.py
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from unidecode import unidecode
from .model_geographic_category import GeographicCategory
from .model_geographic_division import GeographicDivision


class GeographicPlace(TranslatableModel):
    id = models.AutoField(primary_key=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=255, null=True, blank=True),
        slug=models.SlugField(max_length=255, blank=True),
    )
    longitude = models.FloatField()
    latitude = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    category = models.ForeignKey(GeographicCategory, on_delete=models.SET_DEFAULT, default=1)
    admin_division = models.ForeignKey(GeographicDivision, on_delete=models.CASCADE, related_name='places')
    location = gis_models.PointField(geography=True, null=True, blank=True)

    class Meta:
        verbose_name = "Geographic Place"
        verbose_name_plural = "Geographic Places"
        indexes = [
            models.Index(fields=['longitude', 'latitude']),
        ]

    def __str__(self):
        name = self.safe_translation_getter('name', any_language=True)
        return f"{name or 'Unnamed Place'} ({self.latitude}, {self.longitude})"

    def clean(self):
        if not self.admin_division:
            raise ValidationError('Place must be associated with a GeographicDivision.')

        # Validate latitude and longitude
        if not (-90 <= self.latitude <= 90):
            raise ValidationError('Latitude must be between -90 and 90 degrees.')
        if not (-180 <= self.longitude <= 180):
            raise ValidationError('Longitude must be between -180 and 180 degrees.')

        # Ensure no more than six decimal places
        self.latitude = round(self.latitude, 6)
        self.longitude = round(self.longitude, 6)

    def save(self, *args, **kwargs):
        self.clean()
        self.location = Point(self.longitude, self.latitude, srid=4326)
        if not self.elevation:
            self.elevation = 0

        if not self.pk:
            super().save(*args, **kwargs)

        for lang in self.get_available_languages():
            lang_code = lang if isinstance(lang, str) else lang[0]
            self.set_current_language(lang_code)
            if not self.safe_translation_getter('name', any_language=True):
                self.name = "To Be Defined"
            if not self.safe_translation_getter('slug', any_language=True):
                self.slug = slugify(unidecode(self.safe_translation_getter('name', any_language=True)))

        super().save(*args, **kwargs)
