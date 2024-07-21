from rest_framework import serializers
from geography.models import GeographicPlace, GeographicDivision


class GeographicDivisionForUrlSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = GeographicDivision
        fields = ['slug', 'parent']

    def get_parent(self, obj):
        if obj.parent:
            return GeographicDivisionForUrlSerializer(obj.parent).data
        return None


class GeographicPlaceWithUrlSerializer(serializers.ModelSerializer):
    admin_division = GeographicDivisionForUrlSerializer()
    url = serializers.SerializerMethodField()

    class Meta:
        model = GeographicPlace
        fields = ['name', 'latitude', 'longitude', 'slug', 'admin_division', 'url']

    def get_url(self, obj):
        admin_division = obj.admin_division

        if not admin_division or not admin_division.parent or not admin_division.parent.parent or not admin_division.parent.parent.parent:
            return None

        city_slug = obj.slug
        subregion_slug = admin_division.slug
        region_slug = admin_division.parent.slug
        country_slug = admin_division.parent.parent.slug
        continent_slug = admin_division.parent.parent.parent.slug

        return f"/weather/{continent_slug}/{country_slug}/{region_slug}/{subregion_slug}/{city_slug}/"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['url'] is None or not instance.confirmed:
            return None
        return representation
