# api/views/view_division.py

import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from geography.models import GeographicDivision
from api.serializers.serializer_division import GreekMunicipalitySerializer  # Corrected import path

# Configure logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
def greek_municipalities(request):
    logger.info(f"Request received with method: {request.method}")
    logger.info(f"Request headers: {request.headers}")
    logger.info(f"Request query params: {request.query_params}")

    municipalities = GeographicDivision.objects.filter(level_name="Municipality")
    serializer = GreekMunicipalitySerializer(municipalities, many=True)
    return Response(serializer.data)
