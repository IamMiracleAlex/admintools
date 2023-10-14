from classification.models import Node
from django.conf import settings

def bulk_approve(modeladmin, request, queryset):
    sub_data = {}
    for sub in queryset:
        sub.status = "approved"
        sub.save()

        sub_name = sub.subcategory_id.title
        department = sub.subcategory_id.parent.parent.title
        bigquery_table = sub.client.bigquery_table
        countries = [country.name for country in sub.countries.all()]
        parent_bigquery_table = settings.PARENT_BIGQUERY_TABLE

        sub_data[sub_name] = {
            "department": department,
            "bigquery_table": bigquery_table,
            "parent_bigquery_tabble": parent_bigquery_table,
            "countries": countries
        }
    
    # Todo Trigger airflow dag from here
    # trigger_dag(sub_data)

       