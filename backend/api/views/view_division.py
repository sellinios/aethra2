# api/views/view_division.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from geography.models import GeographicDivision
from api.serializers.serializer_division import GreekMunicipalitySerializer

@api_view(['GET'])
def greek_municipalities(request):
    regions = GeographicDivision.objects.filter(level_name='Region').order_by('name')
    regions_data = []
    for region in regions:
        municipalities = GeographicDivision.objects.filter(parent=region, level_name='Municipality').order_by('name')
        region_data = {
            'name': region.name,
            'municipalities': GreekMunicipalitySerializer(municipalities, many=True).data
        }
        regions_data.append(region_data)
    return Response(regions_data)
