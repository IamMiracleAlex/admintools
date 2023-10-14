from django.core.management.base import BaseCommand
from classification.models import Node, FacetValue, NodeFacetRelationship

class Command(BaseCommand):
    help = 'Assign all facets to all nodes without existing relationships'

    def handle(self, *args, **kwargs):
        facets = FacetValue.objects.all()
        counter = facets.count()
        

        for facet in facets:
            counter -= 1
            print(f"{counter} remaining")
            nids = NodeFacetRelationship.objects.filter(facet=facet).values("node_id")
            remainders = Node.objects.all().exclude(id__in=nids)

            NodeFacetRelationship.objects.bulk_create([NodeFacetRelationship(node=node, facet=facet, has_facet="sometimes") for node in remainders])




