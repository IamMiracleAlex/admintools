from django.db import models
from django.db.models import fields
from rest_framework import serializers

from annotation.serializers import ClientSerializer
from users.serializers import ClientUserSerializer

from .models import Manufacturer, Node, FacetValue, FacetCategory, NodeFacetRelationship, SKUMapper
from .utils import upward_inherit_facets, downward_inherit_facets


class FacetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacetValue
        fields = "__all__"


class FacetCategorySerializer(serializers.ModelSerializer):
    facets = FacetSerializer(many=True, read_only=True)

    class Meta:
        model = FacetCategory
        fields = "__all__"
        read_only_fields = ("facets",)


class NodeFacetRelationSerializer(serializers.ModelSerializer):
    facet = serializers.PrimaryKeyRelatedField(queryset=FacetValue.objects.all())

    class Meta:
        model = NodeFacetRelationship
        fields = ("facet", "has_facet")


class NodeSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), allow_null=True)
    facet_properties = NodeFacetRelationSerializer(many=True, allow_null=True, write_only=True)

    class Meta:
        model = Node
        fields = ("id","title", "description","facet_properties","level", "parent")

    def create(self, validated_data):

        facets = validated_data.pop('facet_properties', None)
        node = Node.objects.create(**validated_data)

        if facets:
            self.assign_facets(node, facets)

        return node

    def update(self, instance, validated_data):

        facets = validated_data.pop('facet_properties', None)

        for attr, value in validated_data.items(): 
            setattr(instance, attr, value)      
        instance.save()

        if facets:
            self.assign_facets(instance, facets)

        return instance

    def assign_facets(self, node, facets):
    
        for facet in facets:
            #Using filter and .first() rather than .get() so the system doesn't break
            #if multiple relationships exist or none exists at all
            relationship = node.facet_properties.filter(facet=facet["facet"]).first()
            if relationship:
                relationship.has_facet = facet["has_facet"]
                relationship.save()
            else:
                node.facet_properties.create(**facet)
            
            downward_inherit_facets(node, facet)
            upward_inherit_facets(node, facet)


class FacetPropertySerializer(serializers.Serializer):
    facet = serializers.PrimaryKeyRelatedField(queryset=FacetValue.objects.all())
    has_facet = serializers.ChoiceField(choices=NodeFacetRelationship.OPTIONS)


class BulkAssignFacetSerializer(serializers.Serializer):
    nodes = serializers.PrimaryKeyRelatedField(many=True, queryset=Node.objects.all())
    facets = FacetPropertySerializer(many=True)

    def create(self, validated_data):
        """
        This method handles bulk facets assignment. it gets called when the serializers save method is called
        """
        nodes = validated_data["nodes"]
        #Merge all descendants into a single queryset using the union method and get their ID's
        descendants = Node.objects.none().union(*[node.get_descendants(include_self=True) for node in nodes]).values("id")

        for facet in validated_data["facets"]:
            relationships = NodeFacetRelationship.objects.filter(facet=facet["facet"], node__in=nodes)
            relationships.update(has_facet=facet["has_facet"])

            #Fetch all descendant relationships for this facet using the combined queryser and perform a bulk update
            child_relationships = NodeFacetRelationship.objects.filter(facet=facet["facet"], node_id__in=descendants)
            child_relationships.update(has_facet=facet["has_facet"])

        return validated_data


class NodeToSKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ("id", "title")


class SKUMapperSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = SKUMapper
        fields = "__all__"


class SKUMapperListSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(source='manufacturer.name', read_only=True)
    node_hierarchy = serializers.SerializerMethodField()
    
    class Meta:
        model = SKUMapper
        fields = ("id", "sku_id", "product_name", "manufacturer", "description", "node_hierarchy", "client")
    
    def get_node_hierarchy(self, obj, **kwargs):
        levels = {0: "department", 1: "category", 2: "sub_category", 3: "subset"}
        data = []
        if obj.hierarchy_mapping:
            for node in obj.hierarchy_mapping.get_ancestors(include_self=True):
                data.append(node.title)
            # I need the list difference between the available levels and the returned 
            # hierarchy_levels
        level_diff = len(levels.values()) - len(data)
        if level_diff > 0:
            for i in range(level_diff):
                data.append("") # just pass an empty string to fill lower levels if any
        return data

class SKUClientMapperSerializer(serializers.ModelSerializer):
    """
    A serializer to display available SKU mapper for clients with their respective summaries.
    """
    name = serializers.CharField()
    mapped_sku = serializers.IntegerField()
    uploaded_sku = serializers.IntegerField()
    last_uploaded = serializers.DateTimeField()
    last_modified = serializers.DateTimeField()
    clientuser = ClientUserSerializer(many=True, read_only=True, source="clientuser_set")
    
    class Meta:
        model = SKUMapper
        fields = (
            'id', 'name', 'mapped_sku', 'uploaded_sku', 
            'last_uploaded', 'last_modified', 'clientuser'
          )


class NodeChangeFeedSerializer(serializers.ModelSerializer):
    history_user = serializers.CharField(source="history_user.email", read_only=True)
    history_type = serializers.CharField(source="get_history_type_display", read_only=True)
    node_ids = serializers.JSONField(required=True, write_only=True)
    history_date = serializers.DateTimeField(read_only=True)
    title = serializers.CharField(max_length=100, read_only=True)

    def restore(self):
        count = 0
        node_ids = self.validated_data['node_ids']
        queryset = Node.objects.all_nodes().filter(pk__in=node_ids)
        for node in queryset:
            if node.history.exists():
                earliest_node = node.history.earliest()
                earliest_node.instance.save()
                count += 1
        return count         
    class Meta:
        model = Node.history.model
        fields = "__all__"


class FacetChangeFeedSerializer(serializers.ModelSerializer):
    history_user = serializers.CharField(source="history_user.email", read_only=True)
    history_type = serializers.CharField(source="get_history_type_display", read_only=True)
    history_date = serializers.DateTimeField(read_only=True)
    label = serializers.CharField(max_length=100, read_only=True)
    facet_category = serializers.CharField(source="category.title", read_only=True)
    facet_ids = serializers.JSONField(required=True, write_only=True)

    class Meta:
        model = FacetValue.history.model
        fields = "__all__"

    def restore(self):
        count = 0
        facet_ids = self.validated_data['facet_ids']
        queryset = FacetValue.objects.filter(pk__in=facet_ids)
        for facet in queryset:
            if facet.history.exists():
                earliest_facet = facet.history.earliest()
                earliest_facet.instance.save()
                count += 1
        return count


class NodeFacetRelationshipChangeFeedSerializer(serializers.ModelSerializer):
    history_user = serializers.CharField(source="history_user.email", read_only=True)
    history_type = serializers.CharField(source="get_history_type_display", read_only=True)
    history_date = serializers.DateTimeField(read_only=True)
    has_facet = serializers.CharField(max_length=10, read_only=True)
    hierarchy = serializers.SerializerMethodField()
    facet_value = serializers.CharField(source="facet.label", read_only=True)
    facet_category = serializers.CharField(source="facet.category.title", read_only=True)
    hierarchy = serializers.CharField(source="node.canonical_title", read_only=True)
    relationship_ids = serializers.JSONField(required=True, write_only=True)

    class Meta:
        model = NodeFacetRelationship.history.model
        fields = "__all__"

    def restore(self):
        count = 0
        relationship_ids = self.validated_data['relationship_ids']
        queryset = NodeFacetRelationship.objects.filter(pk__in=relationship_ids)
        for rship in queryset:
            if rship.history.exists():
                earliest_rship = rship.history.earliest()
                earliest_rship.instance.save()
                count += 1
        return count


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = ("id", "name")