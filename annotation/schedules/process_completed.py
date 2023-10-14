from celery import shared_task

from annotation.models import Url, Step
from classification.utils import node_from_hierarchy_string


class ProcessCompleted:
    '''Process completed tasks'''

    def handle(self):

        #The last Step contains all annotation data. Other steps are just snapshots
        final_steps = Step.objects.filter(step="entities_classification",
                                          completed=True,
                                          task__mode="annotator",
                                          task__url__known=False,
                                          task__state="completed")

        for step in final_steps:
            data = step.step_data
            products = []
            entities = []
            task = step.task
            url = task.url.url
            
            if not data["entitiesClassified"]:
                print("Incomplete data")
                step.task.delete() #Not sure if we wanna do this

                continue #jump to next task
                    
            products = data['products']

            for entity in data['entities']:
                e = []
                # OUR ENTITIES AT THIS POINT IS AN ARRAY OF PRODUCT OF ID'S
                # WE CONVERT THEM TO THE FULL PRODUCT OBJ HERE
                for i in entity:
                    product = self.find_product(products, i)
                    if product:
                        e.append(product)
                entities.append(e)

            count = 0
            for classified in data["entitiesClassified"]:
                entities[count][0]["classification"] = classified
                count = count + 1

            for entity in entities:
                entity_obj = self.get_entity_obj(entity, url)
                facet_properties = self.get_facet_properties(entity, url)
                if entity_obj:

                    #Save intents to rds
                    url_obj = Url.objects.get(url=entity_obj['url'])
                    intent_data = url_obj.intent_data.create(**entity_obj)
                    for product in entity:
                        try:
                            intent_data.selected_products.create(product=product['name'], intent=product['intent'])
                        except:
                            pass

                    facet_properties = self.get_facet_properties(entity, url)
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

    def get_intent(self, entity):
        intent = 0
        count = 0
        for product in entity: 
            intent += int(product["intent"])
            count += 1
            
        intent_average = intent / count
        return int(round(intent_average))
    

    def get_entity_obj(self, entity, url):
        main = entity[0]
        if "classification" not in main or "name" not in main:
            print("Was missing name or classification!")
            return None
        
        result = {
            "url": url,
            "department": main["classification"]["selectedDepartment"],
            "category": main["classification"]["selectedCategory"],
            "subcategory": main["classification"]["selectedSubcategory"],
            "subset": main["classification"]["selectedSubset"],
            "intent": self.get_intent(entity),
        }

        return result

    def get_facet_properties(self, entity, url):

        main = entity[0]["classification"]
        entity_facets = []

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
                            "entity_intent": self.get_intent(entity),
                            "facet_intent": self.get_intent(entity),
                            "facet_type": "annotated",
                        }
                        entity_facets.append(result)
        else:
            pass

        #Include facets marked "always" on the hierarchy"
        levels = ["selectedDepartment", "selectedCategory", "selectedSubcategory", "selectedSubset"]
        hierarchy_string = " | ".join([main[level] for level in levels if main[level]])
        node = node_from_hierarchy_string(hierarchy_string)
        if node:
            for relationship in node.facet_properties.filter(has_facet="always"):
                result = {
                        "facet": relationship.facet.label,
                        "entity_intent": self.get_intent(entity),
                        "facet_intent": self.get_intent(entity),
                        "facet_type": "default",
                    }
                entity_facets.append(result)

        return entity_facets

    def find_product(self, products, idx:str):
        result = {}
        for product in products:
            if str(product["id"]) == str(idx):
                result = product
                break
        return result


@shared_task
def process():
    process_tasks = ProcessCompleted()
    process_tasks.handle()
    return True
