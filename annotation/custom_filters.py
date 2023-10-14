from django.db.models import Q
from .models import Task, Url


def url_type_filter(queryset, value):
    '''
    A filter to take care of the url types in the 
    urleditor during filter
    '''
    if value == 'raw':
        queryset =  queryset.filter(status='amber')
    if value == 'tbaq':
        queryset = queryset.intersection(Url.objects.tbaq())
    if value == 'known':
        queryset = queryset.filter(known=True)
    if value == 'bad':
        BAD_URLS = [task.url.url for task in Task.objects.filter(state="bad_url")]
        queryset = queryset.filter(url__in=BAD_URLS)
    return queryset