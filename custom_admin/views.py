import csv
import codecs
from datetime import timedelta

from django.db import transaction
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from annotation.models import IntentData, FacetProperty
from classification.models import Node, FacetValue
from custom_admin.utils import get_next_level, trigger_dag, format_last_run_date, DagError
from custom_admin.models import DataRelease


class HandleBulkEdit(LoginRequiredMixin, View):

    def get(self, request):

        data = request.GET
        fields = ["from_department", "from_category", "from_subcategory", "from_subset"]
        matches = {field.lstrip("from_"):data[field] for field in fields if data[field]}
        
        all_data =  IntentData.objects.filter(**matches)
        display_data = all_data[:100]
        html_page = render_to_string(
                            'matches.html',
                            {'intent_data': display_data,
                            'total_count': all_data.count(),
                            'display_count':  display_data.count() },
                            request=request,
                    )
        return JsonResponse({"html_page": html_page})

    def post(self, request):
        if request.FILES:
            file = request.FILES.get('file')
            reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
            sum_rows = 0
            csv_rows = 0
          
            for i in range(2):
                next(reader)    
            
            for row in reader:
                fields = ['department', 'category', 'subcategory', 'subset']               

                # We want to retrieve and update all data before committing to the db and 
                # also revert this block, if an error occurs 
                for row in reader:
                    fields = ['department', 'category', 'subcategory', 'subset']               
                    filters = {fields[i]: row[i] for i in range(len(fields)) if row[i] != '' }
                    intent = IntentData.objects.filter(**filters)
                    sum_rows += intent.count()  # counts number of db rows updated
                    csv_rows = csv_rows + 1 if intent.exists() else csv_rows + 0 # counts number of csv rows processed
                    
                    updates = {fields[i]: row[i+5] for i in range(len(fields)) if row[i+5] != '' }
                    intent.update(**updates)
                
            message = f"{sum_rows} database rows were updated successfully"
            messages.success(request, f"{csv_rows} csv rows were processed")
        else:    
            data = request.POST
            from_fields = ["from_department", "from_category", "from_subcategory", "from_subset"]
            matches = {field.lstrip("from_"):data[field] for field in from_fields if data[field]}
                       
            to_fields = ["to_department", "to_category", "to_subcategory", "to_subset"]
            destination = {}
            for field in to_fields:
                value = data[field]
                if value:
                    matched_node = Node.objects.get(id=value)
                    destination[field.lstrip("to_")] = matched_node.title if matched_node else ""

            facet = data.get('facet')
            if matches and facet:
                facet_label = facet.split(':')[1]
                intent_data = IntentData.objects.filter(**matches)

                if intent_data.exists():
                    if FacetProperty.objects.filter(entity=intent_data.first(), facet=facet_label).exists():
                        messages.warning(request, f'Facet: `{facet_label}` already exists')
                        pass
                    FacetProperty.objects.create(entity=intent_data.first(), facet=facet_label, facet_type='default', entity_intent=1, facet_intent=1)
                    messages.success(request, f'Facet: `{facet_label}` added successfully')


            if matches and destination:
                # update intent data
                intent_data = IntentData.objects.filter(**matches).update(**destination)

                hierarchy = " | ".join(destination.values())
                message = f"Data changed successfully to: {hierarchy}"
            else:
                message = "Please select the correct options to update annotation data"

        messages.success(request, message)
        return redirect("/custom_admin/bulkedit/")


@login_required
def load_extra_data(request):
    # Doing some intial work for the fields
    all_fields = [{f.name:f.name} for f in IntentData._meta.get_fields()]
    node_id = request.GET.get('node_id', '')
    level = request.GET.get('level', None) # need this to keep track of the levels in intent_data
    
    # if it is `to` field we are meant to use a node
    is_to = level.split('_')[-2] == "to"
    level_name = level.split('_')[-1]
    filter_query = None
    next_level = get_next_level(level_name)
    data ={}
    for field in all_fields:
        if level_name in field.keys():
            filter_query = {level_name: node_id}
    if is_to:
        node = Node.objects.get(id=node_id)
        children_list = list(node.get_children().values('id', 'title'))
        data["level"] = node.level
        data["data"] = children_list
    else:
        intent_data = []
        for intent in IntentData.objects.filter(**filter_query).order_by(f'-{next_level}').values_list(next_level, next_level).distinct():
            if intent[1] is not None:
                intent_data.append({"title": intent[1]})   
        data = {"data": intent_data}
    return JsonResponse(data, safe=False)


class HandleFacetBulkEdit(LoginRequiredMixin, View):
    def get(self, request):
        
        facet = request.GET.get('from_facet')
        all_data =  FacetProperty.objects.filter(facet=facet)
        display_data = all_data[:100]
        html_page = render_to_string(
                            'facet_matches.html',
                            {'facet_data': display_data,
                            'total_count': all_data.count(),
                            'display_count':  display_data.count() },
                            request=request,
                    )
        return JsonResponse({"html_page": html_page})

    def post(self, request):
        from_facet = request.POST.get('from_facet')
        to_facet = request.POST.get('to_facet')
        
        if from_facet and to_facet:
            FacetProperty.objects.filter(facet=from_facet).update(facet=to_facet)
            message = f"`{from_facet}` changed successfully to: {to_facet}"
        else:
            message = "Please select the correct data"

        messages.success(request, message)
        return redirect("/custom_admin/facetbulkedit/")           


class HandleDataRelease(LoginRequiredMixin, View):
    
    def get(self, request):
        
        try:
            trigger_dag()
            result = "success"
        except DagError as e:
            print(e)
            result = "failed"
        
        obj = DataRelease.objects.create(result=result, last_run = timezone.now())
        
        last_run = format_last_run_date(obj.last_run)

        return JsonResponse({
            "last_run": last_run,
            "result": obj.result
        })

@login_required
def get_row_data(request):
   
    obj = DataRelease.objects.last()
    if obj is None:
        obj = DataRelease.objects.create()

    last_run = format_last_run_date(obj.last_run)
    
    result = obj.result

    return JsonResponse({
        "last_run": last_run,
        "result": result
    })