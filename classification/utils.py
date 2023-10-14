import csv, io
import os
import threading
import boto3
import urllib
from django.conf import settings
from django.utils import timezone
from django.db.models.query import Prefetch
from .models import FacetValue, Node, NodeFacetRelationship, FacetCategory, SKUMapper
from django.db import transaction
#Want to maintain zappa's async function if in a lambda environment
if settings.IS_LAMBDA_ENVIRONMENT:
    from zappa.asynchronous import task
else:
    from celery import shared_task as task


TEMP_PATH = lambda x:os.path.join("/tmp/", x)

def node_to_dict(node, include_facets=[]):

    result = {
        'id': node.id,
        'title': node.title,
        'description':node.description,
        'parent':node.parent_id,
        'created_at': node.created_at,
        'children': [node_to_dict(child, include_facets=include_facets) for child in node.get_children()]
    }
    if include_facets:
        result["facets"] = node.get_facets(include_facets=include_facets)

    return result


def node_from_hierarchy_string(hierarchy_string):
    try:
        node_list = [node.strip() for node in hierarchy_string.split("|")]
        level = len(node_list) -1
        last_node = node_list[-1]
        last_node_parent = Node.objects.filter(title=node_list[-2], level=level-1).first()
        node_object = Node.objects.filter(title=last_node, level=level, parent=last_node_parent)

        return node_object.first()
    except Exception as e:
        print(e)
        return None


def upward_inherit_facets(node, facet):
    """
    If all sibling nodes have same relationship with a facet, then the parent node can assume same
    facet relationship. Otherwise, defaults to sometimes
    """
    for parent_node in node.get_ancestors():
        #Fetch existing relationship..
        relationship = parent_node.facet_properties.filter(facet=facet["facet"]).first()

        if relationship:
            all_child_relationships = NodeFacetRelationship.objects.filter(node__parent=parent_node).exclude(id=parent_node.id)
            if all([relation.has_facet == facet["has_facet"] for relation in all_child_relationships]):
                relationship.has_facet = facet["has_facet"]
            else:
                relationship.has_facet = "sometimes"
            relationship.save()
        else:
            parent_node.facet_properties.create(**facet)


def downward_inherit_facets(node, facet):
    """
    assign same facets to all descendants of a node
    """
    descendants = node.get_descendants()
    child_relationships = NodeFacetRelationship.objects.filter(facet=facet["facet"], node__in=descendants)
    child_relationships.update(has_facet=facet["has_facet"])


def is_allowed(user, group_names=[]):
    """
    Checks if the user is in a list of group names or a is super admin
    """
    if settings.ENVIRONMENT in ("staging", "dev"):#Grant full access on staging & locql
        return True
    else:
        user_group = [group['name'].lower() for group in user.groups.all().values('name')]
        return any([elem.lower() for elem in user_group if elem in group_names])


def build_extract(node):
    #NB: It is important to keep ordering of prefetch cache and facets same.
    #otherwise the rows get out of sync
    data = []    
    facets = FacetValue.objects.select_related("category").order_by("id")
    facets_count = facets.count()
    header = ["Node", "ID"] + [facet.canonical_label for facet in facets]
    nodes = node.get_descendants().prefetch_related(Prefetch(
        "facet_properties", queryset=NodeFacetRelationship.objects.order_by("facet_id")))

    for node in nodes:
        row = [node.title, node.id]
        facet_properties = node.facet_properties.all()

        #If this node has a relationship with all facet values, we can go ahead and loop through all
        #Via list comprehension which is wayy faster
        if facets_count == facet_properties.count():
            row.extend([relationship.has_facet for relationship in facet_properties])
            
        #Otherwise, we loop through each facets to find the missing relationships and  fill appropriately as "-"
        #Which is slower but neccessary to ensure correct output
        else:
            for facet in facets:
                has_facet = "-"
                relationship = node.facet_properties.filter(facet=facet).first()
                if relationship:
                    has_facet = relationship.has_facet
                row.append(has_facet)

        data.append(row)

    return header, data


@task
def build_extract_async(node_id, email):

    node = Node.objects.get(id=node_id)
    header, data = build_extract(node)
                    
    title = get_extract_title(node)
    temp_path = os.path.join("/tmp/", title)

    with open(temp_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    bucket_name = "facet-extracts"
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(bucket_name).upload_file(
        Filename=temp_path, Key=title, ExtraArgs={'ACL': 'public-read'})

    download_link = urllib.parse.quote(f"{bucket_name}.s3.amazonaws.com/{title}")
    message = f'''
    Hello {email}, here's a link to download your facet extracts:

    {download_link}

    have a nice day!
    '''

    subject = "Facet extract download"
    send_mail(subject, message, [email])


def send_mail(subject, body, recipient=None):

    client = boto3.client('ses', region_name="us-east-1")

    source='no-reply@mail.centricity.cloud'
    destination={'ToAddresses': recipient}
    message = {
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': body,
            },
        },
        'Subject': {'Charset': 'UTF-8', 'Data': subject}
    }

    return client.send_email(Destination=destination, Message=message, Source=source)

 
def get_extract_title(node):
     return f"Facet extract for {node.title} {timezone.now()}.csv"

@task
def build_facet_category_extract(node_id, email):
    node = Node.objects.get(id=node_id)
    nodes = node.get_descendants(include_self=True)
    values = [option[0] for option in NodeFacetRelationship.OPTIONS]
    data = []
    node_list = list(nodes)#Convert to a list so we can pop out one at a time.

    def get_relationship_values():
        """
        Inner function to be started as a thread.... cos it makes sense
        """
        node_data = []
        while node_list:
            try:
                node = node_list.pop(0)
            except:
                return

            for category in FacetCategory.objects.all():
                row = [node.canonical_title, category, ]
                for value in values:
                    if node.facet_properties.filter(has_facet=value, facet__category=category).exists():
                        row.append("X")
                    else:
                        row.append("-")
                node_data.append(row)
            data.extend(node_data)

    #Spin up 3 threads to work concurrently. Spinning up more is useless in python BTW
    #They'll end up waiting for each other
    threads = [threading.Thread(target=get_relationship_values) for i in range(3)]
    for thread in threads:
        thread.start()

    #Join all threads to main thread. to Wait all for threads to terminate before writing csv.
    #Otherwise you get a nice empty csv
    for thread in threads:
        thread.join()

    title = f"Facet category relationship for {node.title} {timezone.now()}.csv"

    header = ["PATH", "FACET"]
    header.extend(values)

    with open(TEMP_PATH(title), "w") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    bucket_name = "facet-extracts"
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(bucket_name).upload_file(
        Filename=TEMP_PATH(title), Key=title, ExtraArgs={'ACL': 'public-read'})

    download_link = urllib.parse.quote(f"{bucket_name}.s3.amazonaws.com/{title}")
    message = f'''
    Hello {email}, here's a link to download your facet extracts:

    {download_link}

    have a nice day!
    '''

    subject = "Facet extract download"
    send_mail(subject, message, [email])

def sku_import(file):
    # some background check on the uploaded file
    # make sure the file is csv
    if not file.name.endswith('.csv'):
        raise TypeError("Invalid file type")
    if file.multiple_chunks():
        raise MemoryError("File is too large (%.2f MB)" % (file.size/(1000*1000))) 
    paramFile = io.TextIOWrapper(file.file)
    csv_dict = csv.DictReader(paramFile)
    all_skus = list(csv_dict)
    all_count = len(all_skus)
    # Check if header exists. Skip the first entry if true else raise
    # a valueError
    header = ["description", "product_name", "manufacturer"]
    first_row = [cell.lower().strip() for cell in all_skus[0]]
    if not all(cell in first_row for cell in header):
        raise ValueError("Missing a header row in your file")
    
    # construct the skuMapper objects for bulk create
    sku_mapping_objs = [
        SKUMapper(
            client_id=row.get('client'),
            product_name=row.get("product_name"),
            sku_id=row.get("sku_id"),
            manufacturer_id=row.get("manufacturer"),
            description=row.get("description"),
            hierarchy_mapping_id=row.get("hierarchy_mapping") or None,
            product_name_variation=row.get("product_name_variation"),
            sales_quantity=row.get("sales_quantity") or 0,
            sales_value=row.get("sales_value") or 0,
            last_sale=row.get("last_sales") or None
        )
        for row in all_skus if not SKUMapper.objects.filter(sku_id=row.get("sku_id")).exists()
    ]
    imported_sku_count = len(sku_mapping_objs)
    # get the difference of the records in the file and and the records created
    existing_count = all_count - imported_sku_count 
    # commit the new records the db
    
    with transaction.atomic():
        SKUMapper.objects.bulk_create(sku_mapping_objs)
    return imported_sku_count, existing_count

@transaction.atomic
def map_sku(node_id, skus):
    '''map sku(s) to a particular node hierarchy'''
    try:
        # get the list of SKU objects from their ids
        sku_queryset = SKUMapper.objects.filter(id__in=skus) 
        # perform a bulk update with the node id provided
        sku_queryset.update(hierarchy_mapping_id=node_id)
        return True
    except:
        return False


