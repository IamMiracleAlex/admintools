import csv
from itertools import groupby
from operator import itemgetter

from django.db.models import query
from django.http import HttpResponse
from django.db.models import Count, Max, Q
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from mptt.templatetags.mptt_tags import cache_tree_children
from .models import Manufacturer, Node, FacetValue, FacetCategory, NodeFacetRelationship, SKUMapper
from django.contrib.auth.mixins import LoginRequiredMixin
from .paginations import SKUClientMapperPagination, paginate
from classification.serializers import (
    NodeSerializer, 
    FacetSerializer, 
    FacetCategorySerializer, 
    BulkAssignFacetSerializer,
    NodeToSKUSerializer, 
    SKUMapperSerializer,
    SKUClientMapperSerializer,
    ManufacturerSerializer
)
from .utils import build_extract, node_to_dict, build_extract_async, get_extract_title, build_facet_category_extract, map_sku
from .permissions import TaxonomistOrReadOnly
from drf_yasg.utils import swagger_auto_schema

from .paginations import SKUClientMapperPagination
from .permissions import TaxonomistOrReadOnly
from annotation.models import Client
from classification.utils import (
    build_extract, node_to_dict, 
    build_extract_async, get_extract_title,
    build_facet_category_extract, sku_import
)
from classification.models import (
    Node, 
    FacetValue, 
    FacetCategory, 
    NodeFacetRelationship, 
    SKUMapper,
    Manufacturer,
)
from classification import serializers
from classification.permissions import TaxonomistOrReadOnly



class NodeViewset(ModelViewSet):
    serializer_class = serializers.NodeSerializer
    permission_classes = [IsAuthenticated, TaxonomistOrReadOnly]
    queryset = Node.objects.all()
    pagination_class = None
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['level']

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        View the entire nodes as a json tree
        """
        nodes = cache_tree_children(Node.objects.all())
        tree = [node_to_dict(node) for node in nodes]

        return Response(tree)

    @action(detail=True, methods=['get'])
    def treeview(self, request, pk=None):
        """
        View a single node as a json tree with it's children
        """
        node = self.get_object()

        return Response(node_to_dict(node))

    @action(detail=True, methods=['get'])
    def treeview_with_facets(self, request, pk=None):
        """
        View a single node as a json tree with it's children
        """
        node = self.get_object()
        tree = node_to_dict(node, include_facets=["always", "never"])

        return Response(tree)

    @action(detail=True, methods=['get'])
    def facets(self, request, pk=None):
        """
        View facet properties of a single node
        """
        node = self.get_object()
        
        facets = node.get_facets(include_facets="__all__")
        return Response(facets)


    @action(detail=True, methods=['get'])
    def facets_for_ce(self, request, pk=None):
        """
        View facet properties of a single node
        """
        node = self.get_object()
        user_version = self.request.GET.get('version')
       
        facets = node.get_facets(include_facets=["sometimes",])
        if user_version is None:
            response = facets
        else:
            # sort facets by category
            sorted_facets = sorted(facets, key=itemgetter('category'))
            group_facets = {key: list(groups) for key,groups in groupby(sorted_facets, key=itemgetter('category'))}

            category_facets = []
            for facet_category in FacetCategory.objects.all():
                if facet_category.title in group_facets.keys():
                    category = {}
                    category['facets'] = list(group_facets.get(facet_category.title))
                    category['facet_category'] = facet_category.title
                    category['category_type'] = facet_category.facet_type
                    category_facets.append(category)
            response = category_facets

        return Response(response)


    @action(methods=['post'], detail=False)
    def bulk_update(self, request):

        data = {  # we need to separate out the id from the data
            i['id']: {k: v for k, v in i.items() if k != 'id'}
            for i in request.data
        }

        matched_queryset = self.get_queryset().filter(id__in=data.keys())

        for instance in matched_queryset:
            serializer = self.get_serializer(
                instance, data=data[instance.id], partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response({"detail":f"{matched_queryset.count()} Nodes updated"})


    @swagger_auto_schema(request_body=serializers.BulkAssignFacetSerializer)
    @action(methods=['post'], detail=False)
    def bulk_assign_facets(self, request):
        serializer = serializers.BulkAssignFacetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def download_facet_extract(self, request, pk=None):
        node = self.get_object()

        #for large departments > 100, send to background process
        if node.get_descendants().count() > 100:
            build_extract_async.delay(node.id, request.user.email)
            message = f'''
            This department is too large to be downloaded immediately.
            a download link will be sent to your email {request.user.email} once extraction is complete
            '''
            response = Response({"detail":message}, status=status.HTTP_202_ACCEPTED)

        #Otherwise, build and let users download rightaway
        else:
            header, data = build_extract(node)
            file_name = get_extract_title(node)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            writer = csv.writer(response)
            writer.writerow(header)
            writer.writerows(data)
        return response


    @action(methods=['get'], detail=True)
    def download_facet_category_extract(self, request, pk=None):

        node = self.get_object()
        build_facet_category_extract.delay(node.id, request.user.email)
        message =  f"A download link will be sent to your email address: {request.user.email}"

        return Response({"detail":message}, status=status.HTTP_202_ACCEPTED)

    @action(methods=["GET"], detail=False)
    def simple_list(self,request):
        query = request.query_params.get('q')
        queryset = self.queryset
        if query:
            queryset = queryset.filter(title__icontains=query)
        qs_to_process = [{"id": node.id, "title": " --> ".join([n.title for n in node.get_ancestors(include_self=True)])} for node in queryset[:50]]
        serializer = serializers.NodeToSKUSerializer(qs_to_process, many=True)
        return Response(serializer.data)


class FacetViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, TaxonomistOrReadOnly ]
    serializer_class = serializers.FacetSerializer
    queryset = FacetValue.objects.all()
    pagination_class = None
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    
class FacetCategoryViewset(ModelViewSet):
    permission_classes = [IsAuthenticated,TaxonomistOrReadOnly ]
    serializer_class = serializers.FacetCategorySerializer
    queryset = FacetCategory.objects.prefetch_related("facets")
    pagination_class = None
    http_method_names = ['get', 'post', 'patch', 'delete']


@api_view(['GET'])
@permission_classes([IsAuthenticated,TaxonomistOrReadOnly])
def nodes_by_facets_value(request, facet_id):
    has_facet = request.query_params.get('has_facet') # decided to get this from a query_param
    queryset = NodeFacetRelationship.objects.filter(facet_id=facet_id).select_related('node')

    if has_facet is not None:
        queryset = queryset.filter(has_facet=has_facet)
    
    nodes = cache_tree_children([relation.node for relation in queryset])
    tree = [node_to_dict(node) for node in nodes]

    return Response(tree)


class SKUMapperViewset(ModelViewSet):
    """Viewset for the sku mapper endpoints"""
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.SKUMapperSerializer
    queryset = SKUMapper.objects.prefetch_related('client', 'manufacturer')

    @action(detail=False, pagination_class=SKUClientMapperPagination)
    def clients(self, request):   
        clients_queryset = Client.objects.annotate(
            uploaded_sku=Count('skumapper'),
            mapped_sku=Count(
                'skumapper',
                filter=Q(skumapper__hierarchy_mapping__isnull=False)
            ),
            last_uploaded=Max('skumapper__created_at'),
            last_modified=Max('skumapper__updated_at')
        ).order_by('id')

        paginated_qs = self.paginate_queryset(clients_queryset)

        if paginated_qs is not None:
            serializer = serializers.SKUClientMapperSerializer(paginated_qs, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = serializers.SKUClientMapperSerializer(clients_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @paginate
    @action(detail=False, methods=['GET'], pagination_class=SKUClientMapperPagination)
    def single_client_sku(self, request, **kwargs):
        # Get the client_ID from the query_params
        client_id = request.query_params.get('client_id')
        if client_id:
            queryset = self.queryset.filter(client_id=client_id)
            return queryset
        return []

    @action(detail=False, methods=["POST"])
    def import_sku(self, request, **kwargs):
        error_msg = status_code = ""
        if request.FILES:
            try:
                file = request.FILES.get('file')
                # import the records using the sku_import utils function
                new_count, existing_count = sku_import(file) # returns a tuple
                return Response(
                    {
                        "message": f"successfully imported {new_count} skus. found {existing_count} existing records",
                    }, status=status.HTTP_201_CREATED)
            except MemoryError as e:
                error_msg = f"MemoryError: {e}"
                status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            except TypeError as e:
                error_msg = f"TypeError: {e}"
                status_code = status.HTTP_406_NOT_ACCEPTABLE
            except Exception as e:
                error_msg = f"Something went wrong: {e}"
                status_code = status.HTTP_400_BAD_REQUEST
        return Response(error_msg, status=status_code) 
    
    @action(detail=False, methods=["POST"])
    def map_to_hierarchy(self, request, **kwargs):
        if request.method == "POST":
            payload = request.data;
            # destructure the payload to individual keys
            node, sku_list = itemgetter("node", "sku_list")(payload)
            # map the sku using the map_sku utils function
            created = map_sku(node.get('value'), sku_list) # should return a boolean
            if created:
                return Response(f"Successfully mapped {len(sku_list)} skus to {node.get('label')}")
        return Response("Something is not right", status=status.HTTP_406_NOT_ACCEPTABLE)

class NodeChangeFeedView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.NodeChangeFeedSerializer
    queryset = Node.history.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['history_date', 'id', 'title']

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering')
        query = self.request.query_params.get('q')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(hierarchy__department=query) | Q(hierarchy__category=query) \
                    | Q(hierarchy__sub_category=query) | Q(hierarchy__subset=query) 
            )

        if ordering and ordering == 'last_deleted':
            queryset = queryset.filter(history_type='-').order_by('-history_date')
        elif ordering and ordering == 'last_changed':
            queryset = queryset.filter(history_type='~').order_by('-history_date')
        elif ordering and ordering == 'last_added':
            queryset = queryset.filter(history_type='+').order_by('-history_date')
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            count = serializer.restore()
            return Response({'detail': f'{count} data restored successfully', 'status': status.HTTP_200_OK})


class FacetChangeFeedView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.FacetChangeFeedSerializer
    queryset = FacetValue.history.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['history_date', 'id', 'label', 'category']

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering')
        query = self.request.query_params.get('q')

        if query:
            queryset = queryset.filter(
                Q(label__icontains=query) | Q(category__title=query)
            )

        if ordering and ordering == 'last_deleted':
            queryset = queryset.filter(history_type='-').order_by('-history_date')
        elif ordering and ordering == 'last_changed':
            queryset = queryset.filter(history_type='~').order_by('-history_date')
        elif ordering and ordering == 'last_added':
            queryset = queryset.filter(history_type='+').order_by('-history_date')
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            count = serializer.restore()
            return Response({'detail': f'{count} data restored successfully', 'status': status.HTTP_200_OK})


class NodeFacetRelationshipChangeFeedView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.NodeFacetRelationshipChangeFeedSerializer
    queryset = NodeFacetRelationship.history.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['history_date', 'facet', 'has_facet']

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering')
        query = self.request.query_params.get('q')

        if query:
            queryset = queryset.filter(
                Q(facet__label=query) | Q(node__title=query)
            )
        if ordering and ordering == 'last_deleted':
            queryset = queryset.filter(history_type='-').order_by('-history_date')
        elif ordering and ordering == 'last_changed':
            queryset = queryset.filter(history_type='~').order_by('-history_date')
        elif ordering and ordering == 'last_added':
            queryset = queryset.filter(history_type='+').order_by('-history_date')
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            count = serializer.restore()
            return Response({'detail': f'{count} data restored successfully', 'status': status.HTTP_200_OK})


class ManufacturerView(generics.ListCreateAPIView):
    model = Manufacturer
    permission_classes = [IsAuthenticated]
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset
    
    def post(self, request, *args, **kwargs):
        serializer = ManufacturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Created successfully!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

