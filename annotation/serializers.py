from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
from django.conf import settings

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from annotation.models import ( 
    Step, Url, Country, Client, QueueUrlRelationship, Task, DomainPriority, 
    ExtensionVersion, PageView )

from classification.models import Node, FacetValue
from annotation.models import Entity, Product, EntityFacetRelationship


class StepSerializer(serializers.ModelSerializer):
    count = serializers.CharField(source="task.url.page_views")
    url = serializers.CharField(source="task.url.url")
    archived_url = serializers.CharField(source="task.url.archived_url")
    Attributes = serializers.SerializerMethodField()
    hierachy_timestamp = serializers.SerializerMethodField()
    annotation_stats = serializers.SerializerMethodField()

    class Meta:
        model = Step
        fields = ["url", "count","step", "archived_url", 'Attributes', "hierachy_timestamp", "annotation_stats"]

    def get_Attributes(self, obj):
        """
        This is not absolutely neccessary, but i'm trying not to break the chrome extension
        with the new api, so i'm mimmicking the old response.
        'Attributes' is needed by the last 2 steps in the chrome extension to render the sidebar
        it contains data from the previous steps.

        TODO: Clean up redundant/repeated data
        """
        return {
            'completed': [step.step_data for step in obj.task.steps.filter(completed=True)],
            'step':obj.step,
            'step-user':self.context['request'].user.email,
            'url': obj.task.url.url,
            'archived_url': obj.task.url.archived_url
            }
    
    def get_hierachy_timestamp(self, obj):
        #Changed this to a try/except statement cos c few tests were failing
        #TODO: Update test cases instead and let this run as normal
        try:
            timestamp = Node.objects.latest('updated_at').updated_at
        except Node.DoesNotExist:
            timestamp =  timezone.now() #Will always be different hence a download is forced.
        return timestamp

    def get_annotation_stats(self, obj):
        # We don’t want to recalculate these fields for every step. Hence, the condition
        # to only compute it for the first step
        if obj.step=='page_products':
            user = self.context['request'].user
            year, week, _ = timezone.now().isocalendar()

            return {
                'today': user.tasks.filter(state="completed", start_date__day=timezone.now().day).count(),
                'this_week': user.tasks.filter(state="completed", start_date__week=week, start_date__year=year).count(),
                'this_month' : user.tasks.filter(state="completed", start_date__month=timezone.now().month, start_date__year=year).count(),
                'urls_in_queue' : Url.objects.tbaq().count()
            }


class StepSubmitSerializer(serializers.Serializer):

    url = serializers.CharField(required=True)
    step_data = serializers.JSONField()
    step = serializers.ChoiceField(choices=Step.STEPS)

    product_ids = serializers.JSONField(required=False)
    names = serializers.JSONField(required=False)
    xpaths = serializers.JSONField(required=False)
    intents = serializers.JSONField(required=False)
    node_ids = serializers.JSONField(required=False)
    facet_ids = serializers.JSONField(required=False)
    has_facets = serializers.JSONField(required=False)

    def validate_url(self, value):
        try:
            Url.objects.get(url=value)
            return value
        except Url.DoesNotExist:
            raise serializers.ValidationError("Invalid url")

    def process(self):
        '''Process the annotation data'''

        if all(self.validated_data):
            product_ids = self.validated_data.get('product_ids')
            names = self.validated_data.get('names')
            xpaths = self.validated_data.get('xpaths')
            intents = self.validated_data.get('intents')
            has_facets = self.validated_data.get('has_facets')
            
            with transaction.atomic():
                # create products
                products = [Product(product_id=product_ids[i], name=names[i], xpath=xpaths[i], intent=intents[i]) for i in range(len(product_ids))] 

                # SQLITE DB seems to have a problem with bulk creation (running queries in parallel)
                if settings.ENVIRONMENT in ["dev_deployment", "staging_deployment", "prod_deployment"]:
                    products_models = [product.save() for product in products]
                else:
                    products_models = Product.objects.bulk_create(products)
                
                # Get nodes
                nodes = Node.objects.filter(pk__in=self.validated_data.get('node_ids'))
                # get facets
                facets = FacetValue.objects.filter(pk__in=self.validated_data.get('facet_ids'))

                # create entity
                avg_intent = sum(intents) / len(intents)
                entity = Entity.objects.create(avg_intent=avg_intent)

                # m2m fields
                entity.products.add(*products_models)
                entity.classification.add(*nodes)

                # Create facet entity rships
                rships = [EntityFacetRelationship(facet=facets[i], has_facet=has_facets[i], entity=entity) for i in range(facets.count())]
                EntityFacetRelationship.objects.bulk_create(rships)
            
            print("All data returned")
        else:
            raise ValidationError({'detail': 'Incomplete data returned'})
        return 

class TaskResetSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)

    def validate_url(self, value):
        try:
            Url.objects.get(url=value)
            return value
        except Url.DoesNotExist:
            raise serializers.ValidationError("Invalid url")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'short_name']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'beeswax_list', 'start_date', 'end_date']


class UrlSerializer(serializers.ModelSerializer):
    countries = serializers.SerializerMethodField(read_only=True)
    clients = serializers.SerializerMethodField(read_only=True)
    state = serializers.SerializerMethodField(read_only=True)

    def get_countries(self, obj):
        countries = obj.country_set.all()
        data = CountrySerializer(countries, many=True).data
        return data

    def get_clients(self, obj):
        clients = obj.client_set.all()
        return ClientSerializer(clients, many=True).data

    def get_state(self, obj):
        tbaq = True if obj.url in self.TBAQ_URLS else False
        bad = True if obj.url in self.BAD_URL_TASKS else False
        raw = True if obj.status == "amber" else False
        return {
            'tbaq': tbaq,
            'known': obj.known,
            'raw': raw,
            'bad': bad
        }

    class Meta:
        model = Url
        fields = '__all__'    

    def __init__(self, *args, **kwargs):
        super(UrlSerializer, self).__init__(*args, **kwargs)
        self.TBAQ_URLS = list(Url.objects.tbaq().values_list('url', flat=True))
        self.BAD_URL_TASKS = [task.url.url for task in Task.objects.filter(state="bad_url")]


class AddUrlSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=2000, validators=[UniqueValidator(queryset=Url.objects.all(),
                            message="This url already exists" )])
    page_views = serializers.IntegerField(max_value=2147483647, min_value=0)
    status = serializers.ChoiceField(choices=DomainPriority.STATUSES)
    priority = serializers.ChoiceField(choices=Url.PRIORITIES, required=False)
    clients = serializers.JSONField(required=False)
    countries = serializers.JSONField(required=False)


    def create(self, validated_data):
        countries = clients = None
        if validated_data.get('countries'):
            countries = validated_data.pop('countries')
        if validated_data.get('clients'):
            clients = validated_data.pop('clients')

        url = Url.objects.create(**validated_data, last_counted=timezone.now(), events=1)

        if countries or clients:
            pageview = PageView.objects.create(
                number_of_views=validated_data.get('page_views'),
                date=timezone.now())

        if countries:
            for id in countries:
                queue = QueueUrlRelationship.objects.create(
                   events = 1,
                   country_id = id,
                   url_id = url.id,
                )
                queue.page_views.add(pageview)       
        if clients:
            for id in clients:
                queue = QueueUrlRelationship.objects.create(
                   events = 1,
                   client_id = id,
                   url_id = url.id,
                )
                queue.page_views.add(pageview)       
      
        return url


class AssignUrlSerializer(serializers.ModelSerializer):
    clients = serializers.JSONField(required=False)
    countries = serializers.JSONField(required=False)
    status = serializers.ChoiceField(choices=DomainPriority.STATUSES)
    priority = serializers.ChoiceField(choices=Url.PRIORITIES, required=True)    
    
    class Meta:
        model = QueueUrlRelationship
        fields = ['url','status', 'priority', 'clients', 'countries']    


class UrlUpdateSerializer(serializers.Serializer):
    url = serializers.PrimaryKeyRelatedField(queryset=Url.objects.all())
    clients = serializers.JSONField(required=False)
    countries = serializers.JSONField(required=False)
    status = serializers.ChoiceField(choices=DomainPriority.STATUSES)
    priority = serializers.ChoiceField(choices=Url.PRIORITIES, required=True)    
    
   
    def create(self, validated_data):
        countries = clients = None
        if validated_data.get('countries'):
            countries = validated_data.pop('countries')
        if validated_data.get('clients'):
            clients = validated_data.pop('clients')

        url = validated_data.get('url')
        url.status = validated_data.get('status')
        url.priority = validated_data.get('priority')
        url.save()

        queryset = QueueUrlRelationship.objects.filter(url=validated_data.get('url'))
        queryset.delete()

        if countries or clients:
            pageview = PageView.objects.create(
                number_of_views=url.page_views,
                date=timezone.now())

        if countries:
            for id in countries:
                queue = QueueUrlRelationship.objects.create(
                   events = url.events,
                   country_id = id,
                   url = url,
                ) 
                queue.page_views.add(pageview)   
        if clients:
            for id in clients:
                queue = QueueUrlRelationship.objects.create(
                   events = url.events,
                   client_id = id,
                   url = url,
                )  
                queue.page_views.add(pageview)   
    
        return url  


class UrlDeleteResetSerializer(serializers.Serializer):
    url_ids = serializers.JSONField(required=True)

    class Meta:
        fields = ['url_ids']

    def destroy(self):
        url_ids = self.validated_data['url_ids']
        urls = Url.objects.filter(pk__in=url_ids) 
        count = urls.count()

        for url in urls:
            url.delete()       
        return count         

    def reset(self):
        url_ids = self.validated_data['url_ids']
        queryset = Url.objects.filter(pk__in=url_ids)
        count = queryset.count()

        for url in queryset:
            url.known = False
            url.save()
            tasks = url.tasks.all()
            tasks.delete()
        return count


class ExtensionVersionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['version']
        model = ExtensionVersion 