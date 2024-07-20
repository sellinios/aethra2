from django.contrib import admin
from .models import GFSForecast, GFSParameter


def enable_parameters(modeladmin, request, queryset):
    queryset.update(enabled=True)


def disable_parameters(modeladmin, request, queryset):
    queryset.update(enabled=False)


enable_parameters.short_description = 'Enable selected parameters'
disable_parameters.short_description = 'Disable selected parameters'


@admin.register(GFSForecast)
class GFSForecastAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'date', 'hour', 'utc_cycle_time', 'imported_at')
    list_filter = ('date', 'utc_cycle_time')
    search_fields = ('latitude', 'longitude', 'date', 'hour')


@admin.register(GFSParameter)
class GFSParameterAdmin(admin.ModelAdmin):
    list_display = ('number', 'level_layer', 'parameter', 'forecast_valid', 'description', 'enabled', 'last_updated')
    list_filter = ('enabled', 'last_updated')
    search_fields = ('number', 'level_layer', 'parameter', 'forecast_valid', 'description')
    actions = [enable_parameters, disable_parameters]