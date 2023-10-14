from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from functools import wraps
from rest_framework import status
from django.db.models import QuerySet
from .serializers import SKUMapperListSerializer

DEFAULT_PAGE_LIMIT = 10

class SKUClientMapperPagination(PageNumberPagination):
    def get_page_size(self, request):
        self.page_size = request.query_params.get("page_limit", DEFAULT_PAGE_LIMIT)
        return self.page_size

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current'] = self.page.number
        response.data['last_page'] = self.page.paginator.count
        response.data['total_items_on_page'] =  self.page_size
        response.data['total_pages'] = self.page.paginator.num_pages
        return response


def paginate(func):
    '''Custom pagination decorator for our custom actions'''

    @wraps(func)
    def inner(self, *args, **kwargs):
        queryset = func(self, *args, **kwargs)
        try:
            assert isinstance(queryset, (list, QuerySet)), "pagination expects a List or a QuerySet"
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = SKUMapperListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = SKUMapperListSerializer(queryset, many=True)
            return Response(serializer.data)
        except AssertionError as e:
            return Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)
    return inner