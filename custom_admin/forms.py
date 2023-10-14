from django import forms
from django.conf import settings
from itertools import chain

from classification.models import Node, FacetValue
from annotation.models import IntentData, FacetProperty


#Django tries to evaluate these forms during automated checks.
#So we check if this is a test environment before evaluating the queryset
#TODO: There should be a better way
def get_intent_data_departments():
    return (IntentData.objects.order_by("-department").values_list("department", "department").distinct())

def get_taxonomy_departments():
    return Node.objects.filter(level=0)

def facet_choices():
        values = (('{} : {}'.format(facet.category, facet.label), '{} : {}'.format(facet.category, facet.label)) for facet in FacetValue.objects.all())
        blank_choice = (('', '---------'),)
        return tuple(chain(blank_choice, values))

def get_facet_properties():
    return (FacetProperty.objects.order_by("-facet").values_list("facet", "facet").distinct())    

def get_face_values():
    return (FacetValue.objects.order_by("-label").values_list("label", "label").distinct())    


class ClassificationEditorForm(forms.Form):
    from_department = forms.ChoiceField(choices=(), required=True, label='Department', widget=forms.Select(attrs={'onchange': "handleChangeEvent(event, type='from')"}))
    from_category = forms.ModelChoiceField(queryset=Node.objects.none(), label='Category', widget=forms.Select(attrs={'onchange': "handleChangeEvent(event, type='from')"}))
    from_subcategory = forms.ModelChoiceField(queryset=Node.objects.none(), label='Subcategory', widget=forms.Select(attrs={'onchange': "handleChangeEvent(event,type='from')"}))
    from_subset = forms.ModelChoiceField(queryset=Node.objects.none(), label='Subset')
    
    to_department = forms.ModelChoiceField(queryset=None, required=True, label="Department", widget=forms.Select(attrs={'onchange': "handleChangeEvent(event,type='to')"}))
    to_category = forms.ModelChoiceField(queryset=Node.objects.none(), label="Category", widget=forms.Select(attrs={'onchange': "handleChangeEvent(event,type='to')"}))
    to_subcategory = forms.ModelChoiceField(queryset=Node.objects.none(), label="Subcategory", widget=forms.Select(attrs={'onchange': "handleChangeEvent(event,type='to')"}))
    to_subset = forms.ModelChoiceField(queryset=Node.objects.none(), label="Subset")
    facet = forms.ChoiceField(choices=(), required=False, label='Facet')
    
    def __init__(self, *args, **kwargs):
        super(ClassificationEditorForm, self).__init__(*args, **kwargs)
        self.fields['from_department'].widget.choices = get_intent_data_departments()
        self.fields['to_department'].queryset = get_taxonomy_departments()
        self.fields['facet'].widget.choices = facet_choices()


class FacetBulkEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # we do this to prevent caching of fields
        self.fields['from_facet'] = forms.ChoiceField(choices=get_facet_properties(), required=True, label='Facet')
        self.fields['to_facet']  =  forms.ChoiceField(choices=get_face_values(), required=True, label='Facet')
