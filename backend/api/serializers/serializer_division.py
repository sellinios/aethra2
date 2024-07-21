from rest_framework import serializers
from geography.models import GeographicDivision


class GeographicDivisionSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = GeographicDivision
        fields = ['slug', 'parent']

    def get_parent(self, obj):
        if obj.parent:
            return GeographicDivisionSerializer(obj.parent).data
        return None


class GreekMunicipalitySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = GeographicDivision
        fields = ['name', 'slug', 'level_name', 'children', 'url']

    def get_children(self, obj):
        children = GeographicDivision.objects.filter(parent=obj)
        return GreekMunicipalitySerializer(children, many=True).data

    def get_url(self, obj):
        if obj.parent and obj.parent.parent and obj.parent.parent.parent:
            subregion_slug = obj.slug
            region_slug = obj.parent.slug
            country_slug = obj.parent.parent.slug
            continent_slug = obj.parent.parent.parent.slug
            return f"/weather/{continent_slug}/{country_slug}/{region_slug}/{subregion_slug}/"
        return None
