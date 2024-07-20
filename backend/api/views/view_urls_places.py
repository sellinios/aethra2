from rest_framework.decorators import api_view
from rest_framework.response import Response
from geography.models import GeographicPlace
from api.serializers.serializer_urls import GeographicPlaceWithUrlSerializer
from django.utils.translation import gettext as _
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


@api_view(['GET'])
def all_places_with_urls(request, lang_code):
    try:
        search_query = request.GET.get('search', '')
        if search_query:
            places = GeographicPlace.objects.language(lang_code).filter(translations__name__icontains=search_query,
                                                                        confirmed=True)
        else:
            places = GeographicPlace.objects.language(lang_code).filter(confirmed=True)

        # Paginate the queryset
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(places, request)

        # Prepare serialized data
        serializer = GeographicPlaceWithUrlSerializer(result_page, many=True)
        serialized_data = [item for item in serializer.data if item is not None]
        return paginator.get_paginated_response(serialized_data)
    except Exception as e:
        # Return the error message in the current language
        return Response({"error": _("An error occurred: {error}").format(error=str(e))}, status=500)