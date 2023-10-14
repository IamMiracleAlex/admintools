from celery import shared_task

from classification.utils import node_from_hierarchy_string
from annotation.models import Url, Step


@shared_task
def process_completed(step_id):
    step = Step.objects.get(id=step_id)
    _process_completed(step)


def _process_completed(step):
    data = step.step_data
    products = []
    entities = []
    task = step.task
    url = task.url.url

    if not data["entitiesClassified"]:
        print("Incomplete data")
        step.task.delete() #Not sure if we wanna do this
        return

    for entity in data['entities']:
        # OUR ENTITIES AT THIS POINT IS AN ARRAY OF PRODUCT OF ID'S
        # WE CONVERT THEM TO THE FULL PRODUCT OBJ HERE
        e = [get_product(data["products"], product_id) for product_id in entity]
        entities.append(e)

    count = 0
    for classified in data["entitiesClassified"]:
        entities[count][0]["classification"] = classified
        count = count + 1

    for entity in entities:
        entity_obj = get_entity_obj(entity, url)
        if entity_obj:

            #Save intents to rds
            url_obj = Url.objects.get(url=entity_obj['url'])
            intent_data = url_obj.intent_data.create(**entity_obj)
            for product in entity:
                intent_data.selected_products.create(product=product['name'], intent=product['intent'])

            facet_properties = get_facet_properties(entity, url)
            if facet_properties:
                first_facet = True
                for prop in facet_properties:
                    if first_facet:
                        intent_data.facet_properties.create(**prop)
                        first_facet = False
                    else:
                        prop["entity_intent"] = 0
                        intent_data.facet_properties.create(**prop)
    task.url.known = True
    task.url.save()



def get_product(products, idx:str):
    for product in products:
        if str(product["id"]) == str(idx):
            return product

def get_intent(entity):
    intent_sum = sum([int(product["intent"]) for product in entity])
    product_count = len(entity)   
    intent_average = intent_sum / product_count

    return int(round(intent_average))

def get_entity_obj(entity, url):
    main = entity[0]

    if "classification" not in main or "name" not in main:
        print("Missing name or classification!")
        return None
    
    return {
        "url": url,
        "department": main["classification"]["selectedDepartment"],
        "category": main["classification"]["selectedCategory"],
        "subcategory": main["classification"]["selectedSubcategory"],
        "subset": main["classification"]["selectedSubset"],
        "intent": get_intent(entity),
    }

def get_facet_properties(entity, url):

    main = entity[0]["classification"]
    entity_facets = []
    intent = get_intent(entity)

    if "facet" in main:

        facets = main["facet"]
        if isinstance(facets, list):
            for facet in facets:
                #Possible values for has_facet was previously "yes", "no" and "maybe",
                #Until an update which added "always" and "never" options and used number mappings instead.
                #So we check for both current and previously possible values
                #incase this script is used to process older annotations.
                if facet["has_facet"] in ["Yes", "0", "1"]:
                    result = {
                        "facet": facet["facet"],
                        "entity_intent": intent,
                        "facet_intent": intent,
                        "facet_type": "annotated",
                    }
                    entity_facets.append(result)

    #Include facets marked "always" on the hierarchy"
    levels = ["selectedDepartment", "selectedCategory", "selectedSubcategory", "selectedSubset"]
    hierarchy_string = " | ".join([main[level] for level in levels if main[level]])
    node = node_from_hierarchy_string(hierarchy_string)
    if node:
        for relationship in node.facet_properties.filter(has_facet="always"):
            result = {
                    "facet": relationship.facet.label,
                    "entity_intent": intent,
                    "facet_intent": intent,
                    "facet_type": "default",
                }
            entity_facets.append(result)

    return entity_facets