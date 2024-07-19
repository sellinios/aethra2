from django.contrib import admin
from django.utils.text import slugify
from parler.admin import TranslatableAdmin
from unidecode import unidecode
from django.utils import timezone
from .models.model_geographic_place import GeographicPlace
from .models.model_geographic_geocode import GeocodeResult
from .models.model_geographic_category import GeographicCategory
from .models.model_geographic_division import GeographicDivision
from .models.model_geographic_data import GeographicData  # Assuming this is the correct import


@admin.action(description='Update elevation, name, and municipality')
def update_elevation_and_name(modeladmin, request, queryset):
    for place in queryset:
        try:
            now = timezone.now()
            geocode_record, created = GeocodeResult.objects.get_or_create(geographic_place=place)
            needs_update = not geocode_record.geocode_last_updated or (
                        now - geocode_record.geocode_last_updated).days > 30  # Update if older than 30 days

            if needs_update:
                # Update logic without Google Maps
                place.elevation = None
                place.confirmed = False
                place.admin_division = None

            # Save the updated place
            place.save()
            modeladmin.message_user(request, f"Updated place: {place.name}")
        except Exception as e:
            modeladmin.message_user(request, f"Error updating place: {str(e)}", level='error')


@admin.register(GeographicPlace)
class GeographicPlaceAdmin(TranslatableAdmin):
    list_display = ('name', 'longitude', 'latitude', 'elevation', 'confirmed', 'category', 'admin_division')
    search_fields = ('translations__name', 'translations__slug', 'category__translations__name', 'admin_division__name')
    list_filter = ('confirmed', 'category', 'admin_division')
    actions = [update_elevation_and_name]

    fieldsets = (
        (None, {
            'fields': (
            'name', 'slug', 'longitude', 'latitude', 'elevation', 'confirmed', 'category', 'admin_division', 'location')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.safe_translation_getter('name', any_language=True):
            obj.set_current_language('en')  # Assuming 'en' is a default language, adjust if necessary
            obj.name = "To Be Defined"
        if not obj.safe_translation_getter('slug', any_language=True):
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "admin_division":
            kwargs["queryset"] = GeographicDivision.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(GeographicCategory)
class GeographicCategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'slug')
    search_fields = ('translations__name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
    )


@admin.register(GeographicDivision)
class GeographicDivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'level_name', 'parent', 'geographic_data_display')
    search_fields = ('name', 'slug', 'level_name', 'parent__name')
    list_filter = ('level_name', 'parent')

    def geographic_data_display(self, obj):
        return obj.geographic_data

    geographic_data_display.short_description = 'Geographic Data'
