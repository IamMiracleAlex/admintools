import json
from django.core.management.base import BaseCommand
from classification.models import Node

class Command(BaseCommand):
    help = 'Populates rds with hierachy'

    def handle(self, *args, **kwargs):
        
        with open("fixtures/hierachy.json", "r") as hierachy:
            f = json.load(hierachy)
            for node in f:
                self.append_children(node)


    def append_children(self, node, parent=None):

        print(f"Adding {node['title']}")
        parent = Node.objects.create(title=node["title"], parent=parent)
        if node["children"]:
            for child in node["children"]:
                self.append_children(child, parent)

        return 0
                
