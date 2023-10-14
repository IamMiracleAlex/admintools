from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from simple_history import register as simple_history_register
from simple_history.signals import pre_create_historical_record

from users.models import User

#Want to maintain zappa's async function if in a lambda environment
if settings.IS_LAMBDA_ENVIRONMENT:
    from zappa.asynchronous import task
else:
    from celery import shared_task as task


class NodeManager(TreeManager):

    def get_queryset(self):
        """return only the active nodes
        """        
        return super(NodeManager, self).get_queryset().filter(status='active')
        
    def all_nodes(self):
        """return all nodes
        """        
        return super(NodeManager, self).get_queryset().all()
    
    def deleted(self):
        """return soft deleted nodes
        """        
        return super(NodeManager, self).get_queryset().filter(status='deleted')


class TimestampModel(models.Model):
    """
    adds a 'created' and 'updated' timestamp field
    to all models that inherit from it
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class HierarchyHistoricalModel(models.Model):
    """
    Abstract model for node history models tracking the hierarchy.
    """
    hierarchy = models.JSONField(null=True)

    class Meta:
        abstract = True

class FacetCategory(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    FACET_TYPE = (
        ('single', 'single'),
        ('multi', 'multi'),
        ('boolean', 'boolean')
    )
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    facet_type = models.CharField(max_length=100, blank=True, choices=FACET_TYPE, default='boolean')

    class Meta:
        verbose_name_plural = "Facet Categories"
        ordering = ("title",)

    def __str__(self):
        return self.title

class FacetValue(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, 
    # Please see the readme for more information

    category = models.ForeignKey(FacetCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name="facets")
    label = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("category","label",)

    def __str__(self):
        return self.label

    @property
    def canonical_label(self):
        '''
        Just the title with the category prepended for easier identification
        '''
        return f"{self.category.title if self.category else ''}:{self.label}"
        
    
class Node(MPTTModel, TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    NODE_STATUS = (
        ('active', 'active'),
        ('deleted', 'deleted')
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    facets = models.ManyToManyField(FacetValue, through="NodeFacetRelationship")
    status = models.CharField(max_length=50, choices=NODE_STATUS, default='active')
    objects = NodeManager()
    
    class Meta:
        unique_together = [("title", "parent", "status"),]
        ordering = ("title",)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        self.status = 'deleted'
        self.save()
    
    def hard_delete(self):
        super(Node, self).delete()
        
    def get_hierarchy(self):
        hierarchy = {0: 'department', 1: 'category', 2: 'sub_category', 3: 'subset'}
        family_list = list(self.get_family().values('title', 'level'))
        data = {hierarchy[family['level']]: family['title'] for family in family_list }
        return data

    @property
    def canonical_title(self):
        return " | ".join([parent.title for parent in self.get_ancestors(include_self=True)])


    def get_facets(self, include_facets=[]):
        """
        Returns facets with values as in "included facets" or all possible facets if the __all__
        flag is used
        """
        facets = []
        options = [option[0] for option in NodeFacetRelationship.OPTIONS]

        if include_facets == "__all__":
            include_facets = options

        elif not all([option in options for option in include_facets]):
            raise ValueError("Included facets contains an invalid facet value")

        for relation in self.facet_properties.select_related("facet__category").all():
            if relation.has_facet in include_facets:
                facet = {}
                facet["id"] = relation.facet_id
                facet["category"] = relation.facet.category.title if relation.facet.category else ""
                facet["label"] = relation.facet.label
                facet["description"] = relation.facet.description
                facet["has_facet"] = relation.has_facet
                facets.append(facet)

        return facets


class NodeFacetRelationship(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    OPTIONS = (
        ("always", "always"),
        ("sometimes", "sometimes"),
        ("never", "never")
    )
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="facet_properties")
    facet = models.ForeignKey(FacetValue, on_delete=models.CASCADE, related_name="related_nodes")
    has_facet = models.CharField(max_length=10, blank=False, choices=OPTIONS)

    def __str__(self):
        return f"{self.node.title}:{self.facet.label} ==> {self.has_facet}"


class TaxonomyEditor(Node):
    """
    Not an actual model, Django doesn't allow registering a single model more than once
    so we use this as a proxy so we can add a custom hierachy editor to the admin site
    """
    class Meta:
        proxy = True
        verbose_name_plural = "Taxonomy Editor"
        
class TaxonomyFeed(Node):
    """
    Not an actual model, Django doesn't allow registering a single model more than once
    so we use this as a proxy so we can add a custom hierachy editor to the admin site
    """
    class Meta:
        proxy = True
        verbose_name_plural = "Taxonomy Feed"

class HierarchyJson(models.Model):
    """
    The data column of this model gets returned everytime there's a call to treeview
    on the nodes. A new object is created everytime a node is created or a facet is added to a node
    """
    timestamp = models.DateTimeField(auto_now=True)
    data = models.JSONField()
    editor = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.timestamp}"

class DeletedNode(Node):
    """
    Proxy model to show deleted nodes
    """
    class Meta:
        proxy = True
        verbose_name_plural = "Recently deleted nodes"


class SKUMapper(TimestampModel):
    """
    Model for mapping client SKUs to node hierarchy data
    """
    client = models.ForeignKey('annotation.Client', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    sku_id = models.CharField(max_length=50)
    manufacturer = models.ForeignKey('Manufacturer', blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, default="")
    hierarchy_mapping = models.ForeignKey('Node', null=True, blank=True, on_delete=models.CASCADE, help_text="node hierarchy data")
    product_name_variation = models.CharField(max_length=200, blank=True, default="")
    sales_quantity = models.IntegerField(blank=True, default=0)
    sales_value = models.IntegerField(blank=True, default=0)
    last_sale = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.product_name} --> {self.sku_id}'
    
    class Meta:
        ordering = ('-created_at',)

class SKUMapperEditor(SKUMapper):
    """
    This to add a custom SKU Mapping editor to the admin site like we did for 
    the taxonomy editor
    """
    class Meta:
        proxy = True
        verbose_name = "SKU Mapper Editor"
        verbose_name_plural = "SKU Mapper Editor"

class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('name',)

simple_history_register(Node, bases=[HierarchyHistoricalModel,])
simple_history_register(FacetValue)
simple_history_register(FacetCategory)
simple_history_register(NodeFacetRelationship)



@receiver(post_save, sender=FacetValue)
@receiver(post_save, sender=Node)
def assign_existing_facets_to_new_nodes(sender, instance, created, **kwargs):
    """
    This signal gets triggered when a new node or facet is created
    and assigns existing facets to the new node or new facet to existing nodes.
    """
    if created:
        if sender == Node:
            perform_bulk_assign(node_id=instance.id)
        elif sender == FacetValue:
            perform_bulk_assign(facet_id=instance.id)


@task
def perform_bulk_assign(node_id=None, facet_id=None):
    if any([node_id, facet_id]):
        bulk = []
        if node_id:
            node = Node.objects.get(id=node_id)
            parental_facets = node.parent.facet_properties.all() if node.parent else None
            for facet in FacetValue.objects.all():
                has_facet = "never"
                parental_relationship = parental_facets.filter(facet=facet).first() if node.parent else None
                if parental_relationship:
                    has_facet = parental_relationship.has_facet

                bulk.append(NodeFacetRelationship(node=node, facet=facet, has_facet=has_facet))
        elif facet_id:
            facet = FacetValue.objects.get(id=facet_id)
            bulk = [NodeFacetRelationship(node=node, facet=facet, has_facet="never") for node in Node.objects.all()]

        NodeFacetRelationship.objects.bulk_create(bulk)

    else:
        raise ValueError("perform_bulk_assign must be called with either node_id or facet_id")


@receiver(pre_create_historical_record, sender=Node.history.model)
def add_history_hierarchy(sender, **kwargs):
    history_instance = kwargs['history_instance']
    instance = kwargs['instance']
    history_instance.hierarchy = instance.get_hierarchy()