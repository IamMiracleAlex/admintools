# Annotation API

#Setting Up:

1.  clone the repository
2.  create a virtual environment running python 3.6 (or above)
    https://realpython.com/python-virtual-environments-a-primer/#using-virtual-environments

3.  cd into the root of the django project (i.e the path containing manage.py)
4.  install requirements `pip install -r requirements.txt`
5.  Set up your environment variables using any credentials of your choice 
    or use the available defaults present in config/settings.py
6.  Create a local postgres instance (or use an existing one)
7.  Modiy the database credentials in settings to match yours (config/settings.py: line 95-99)
8.  run `python manage.py migrate` to create database tables
9.  run `python manage.py createsuperuser` to create a superuser(An initial user that has access to the admin site)
10. run `python manage.py json_to_sql` to seed the database with Taxonomy data
11. run `python manage.py runserver` to start the development server

The application should now be running on port 8000 on localhost(localhost:8000)
admin site available at localhost:8000


#Development:
1. If your update requires a third party library to function, endeavour to update the requirements.txt file
    with `pip freeze > requirements.txt`. Ensure only needed libraries are added and remove a library no longer in use
    from requirements to avoid overblowing the zip size of the lambda during deployment 

2. If your update requires change in the database, endeavour to generate migrations locally before pushing
    with `python manage.py makemigrations`. Test applying migrations locally and fix possible errors.

3. Provide docstrings and comments that adequately describes your operation/aim/usage

4. To schedule an operation,
    (a) Make it as a management command (https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html)
    (b) All management commands are made available from schedules.py in the project root. So schedule your command
    to run with under events in zappa_settings with function name as `schedules.'your_command'`
    https://github.com/Miserlou/Zappa#scheduling

#React setup (Development)
1. Go to `react/front` folder

2. Execute command `npm install`

3. Execute command `npm run build-local` (This will create a build to run on local machine referencing the local static server)

4. Execute command `npm run serve-static` (Starts the satic files server). When you load `http://192.168.2.223:5000` after this command, the react site will be displayed

5. To view the react site within the django app:

    1. Copy the css and js files from `react/frontend/static/index.html` and paste into `react/templates/hierarchy.html` (replace existing files to ensure the latest css and js are captured). 

    2. From top level of the repo, execute `python manage.py collectstatic`

    3. Execute `python manage.py runserver`. You should now be able to navigate /hierarchy from django app

#React setup (Production)
Assuming you have made changes and are ready to create a production build:

1. Execute command `npm run build`. This builds the css and js files with  s3 path location reference

2. Copy the css and js files from `react/frontend/static/index.html` and paste into `react/templates/hierarchy.html` (replace existing files to ensure the latest css, js and the correct paths are referenced).

3. From top level of the repo, execute `python manage.py collectstatic`

4. App is now ready for deployment

5. Follow django deployment steps 

#Deployment
Deployment is handled by Zappa (https://github.com/Miserlou/Zappa#about)
See the zappa configuration in `zappa_settings.json` in the project root directory
To deploy, ensure all development instructions above are followed and run `zappa update dev`
To invoke a management command on AWS, run `zappa manage dev 'command'` e.g to run migrations after deployment,
run `zappa manage dev migrate`

# New Custom Page in Admin
1. If new page should not be logically grouped with other existing pages, create a new app:
```python manage.py startapp classification```
2. Add new model to classification/models.py.  Make sure meta=true
```
class HierarchyEditor(Node):
    """
    Not an actual model, Django doesn't allow registering a single model more than once
    so we use this as a proxy so we can add annotation statistics to the admin site
    """
    class Meta:
        proxy = True
        verbose_name_plural = "Hierarchy Editor"
```
3. Register new admin screen in classification/admin.py
```
from .models import HierarchyEditor

class HierarchyEditorAdmin(admin.ModelAdmin):
    # expects some indent block
    harry_potter = "wizard"

admin.site.register(HierarchyEditor, HierarchyEditorAdmin)
```

3. New folder in /templates/admin - /classification/hierarchyeditor
4. New template file change_list.html
5. Extend the current Jazzmin main change_list template :
```
{% extends "admin/change_list.html" %}
```
6. Extend or overwrite content blocks in template provided by Jazzmin as needed, 
https://github.com/farridav/django-jazzmin/blob/master/jazzmin/templates/admin/change_list.html



#URL Advanced Search
1. Go to `All URLS` page or The `Url Editor`

2. You can search for urls with a regex pattern

3. To do this, start the search with a `^`

4. An example is `^http(s?)://target.com/`

5. This should match strictly all urls from target.

6. Because all regex searches must start with `^`. To bypass, use        something similar to  `^.*target.com/.*`, which also strictly matches all urls from target


# Using Celery
Please see https://docs.celeryproject.org/en/stable/index.html for more information.

-  Startup Celery worker to receive tasks:

`celery -A config worker -l info`

-  Startup Celery task scheduler:

`celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`

-  To create an async task, do:
```
from celery import shared_task

@shared_task
def funx_name(x, y):
    return x + y
```

-  To create a scheduled task  
place the function in `<app_name>/schedules/<task_name.py>/handle`

-  Add the task to `config/celery.py`

-  Add the module to celery imports in `config/settings.py`


# Protected Models
Some models in the application are referred to as protected.
This is because there are audit tables that depend on these models.

To change, add or remove a field from a protected model, you'll have to update the audit table and audit function attached to such model.

