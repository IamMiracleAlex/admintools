from django.core.management.base import BaseCommand

from annotation.models import Task




class Command(BaseCommand):
    help = 'Fix bad attention'

    def handle(self, *args, **kwargs):

        urls = []
        # add a urls.txt file to the base path
        with open('urls.txt') as f:
            lines = f.readlines()
            for url in lines:
                urls.append(url.strip())
                
        for url in urls:
            tasks = Task.objects.filter(url__url=url)

            for task in tasks:
                for step in task.steps.all():
                    if step.step == 'entities_classification':
                        entities_classified = step.step_data.get('entitiesClassified')
                        entities = step.step_data.get('entities')
                        if not entities and not entities_classified:
                            print("Deleting task for absent of classification data")
                            print(url, "task was deleted")
                            task.delete()
                        elif entities and entities_classified:
                            for i in range(len(entities_classified)):
                                try:
                                    if entities_classified[i].get('selectedDepartment') in [None, 'null', 'Select a Match']:
                                        print("Deleting entity, because of a bad department")
                                        del step.step_data['entitiesClassified'][i]
                                        del step.step_data['entities'][i]
                                        step.save()
                                except Exception as e:
                                    print(task)
                                    #task.delete()
                        else:
                            print(f'The url: "{url}" was not affected')       
        print("Done")    
