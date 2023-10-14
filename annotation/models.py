from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.template.defaultfilters import truncatechars
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from classification.models import FacetValue, TimestampModel

from users.models import User


class DomainPriority(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    STATUSES = (
        ("red", "red"),
        ("amber", "amber"),
        ("green", "green")
    )
    
    domain = models.CharField(max_length=100, null=False, unique=True)
    approximate_urls = models.PositiveIntegerField(blank=True, null=True)
    views = models.PositiveIntegerField(blank=True, null=True)
    last_counted = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=5, choices=STATUSES, default='amber')

    class Meta:
        db_table = "domains"
        verbose_name_plural = "Domain Priority Queue"
        ordering = ["-views"] #Order by highest page_views first
    
    def __str__(self):
        return self.domain


class UrlManager(models.Manager):
    """
    The below query:
    Url.objects.filter(status="green",known=False,annotators_assigned__lt = F("required_annotations"))
    which constitutes the annotation queue appears in several places. To save that much typing, we make a
    custom manager, so you can easily do: Url.objects.tbaq() in place of the above.
    ref: https://docs.djangoproject.com/en/3.0/topics/db/managers/
    """

    def tbaq(self):
        return self.exclude(archived_url="None").filter(
            status="green",
            known=False,
            annotators_assigned__lt=F("required_annotations"),
            ).exclude(archived_url="")

    def fallback_tbaq(self):
        """
        This query serves as a fallback to be used to create tasks temporarily when tbaq is exhausted
        until urls are whitelisted
        """
        print('Now using fallback tbaq')
        #Domains are ordered by highest views first
        top_ten_domains = [domain for domain in DomainPriority.objects.all()[:10]]

        return self.filter(
            known=False,
            domain__in=top_ten_domains,
            annotators_assigned__lt=F("required_annotations")
            ).exclude(archived_url="")
        
        
    
class Url(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    PRIORITIES = ((1, "high"), (2, 'medium'), (3, 'low'))

    GREENlIST_METHODS = (
        ('manual', 'manual'),
        ('autofill', 'autofill'),
        ('scraper', 'scraper')
    )

    url = models.CharField(max_length=2000, blank=False, null=False, unique=True)
    page_views = models.PositiveIntegerField()
    known = models.BooleanField(default=False)
    last_counted = models.DateTimeField(auto_now=False, auto_now_add=False)
    events = models.PositiveIntegerField()
    annotators_assigned = models.PositiveIntegerField(default=0)
    required_annotations = models.PositiveIntegerField(default=1)
    archived_url = models.CharField(max_length=2000, blank=True)
    status = models.CharField(max_length=5, choices=DomainPriority.STATUSES)
    domain = models.ForeignKey(DomainPriority, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="urls")
    priority = models.IntegerField(choices=PRIORITIES, default=2)
    archive_attempt_count = models.PositiveIntegerField(default=0)
    greenlist_method = models.CharField(choices=GREENlIST_METHODS, default="", max_length=100)
    date_greenlisted = models.DateTimeField(null=True)

    objects = UrlManager()

    def __str__(self):
        return self.url

    class Meta:
        db_table = "urls"
        verbose_name_plural = "All URLs"
        ordering = ["priority", "-page_views"] #Order by priority, then highest page_views
        indexes = [
            models.Index(fields=["status"])
        ]

    @property
    def queued(self):
        """
        Boolean to show if a url is in queue or not
        """
        criteria = [
            self.known==False,
            self.annotators_assigned < self.required_annotations,
            self.status == "green",
            #I'm not sure what the actual empty value is,
            #But the point here is it shouldn't be empty.
            self.archived_url != None

            ]
        #The builtin "all" function takes an iterable and returns True if the boolean evaluation of 
        #all items in the iterable is true, otherwise False if any fails

        return all(criteria)


    @property
    def short_url(self):
        """
        Some urls are way too long and distorts view in the admin site.
        Use this property to display truncated url if the length is more than 40 characters
        """
        return truncatechars(self.url, 45)

    @property
    def archived(self):
        """
        A boolean property that specifies if a url has been archived or not
        """
        return self.archived_url != ""


class UrlScraped(TimestampModel):

    text = models.CharField(max_length=10485760, blank=True, null=True)
    url = models.IntegerField(unique=True, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    scraped_vector = models.TextField(blank=True, null=True)  # This field type is a guess.
    scraped_query = models.TextField(blank=True, null=True)  # This field type is a guess.
    suggested_list = models.CharField(max_length=30, blank=True, null=True)
    list_parsing_status = models.CharField(max_length=30, blank=True, null=True)
    instance_score = models.IntegerField(blank=True, null=True)
    original_language = models.CharField(max_length=50, blank=True, null=True)
    original_text = models.CharField(max_length=10485760, blank=True, null=True)


    class Meta:
        db_table = 'urls_scraped'

    def __str__(self):
        try: 
            url = Url.objects.get(id=self.url).url
        except: 
            url = None
        return url or super().__str__()


class Task(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    STATES = (
        ("in_progress", "in_progress"),
        ("completed", "completed"),
        ("bad_url", "bad_url")
    )

    MODES = (
        ("developer", "developer"),
        ("annotator", "annotator")
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="tasks")
    start_date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=15, choices=STATES, default="in_progress")
    url = models.ForeignKey(Url, on_delete=models.DO_NOTHING, related_name="tasks")
    mode = models.CharField(max_length=10, blank=True, null=True, choices=MODES, default="annotator")
    reason_for_skipping_url = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        unique_together = ("user", "url")#No user should annotate a single url more than once
        db_table = "tasks"
        ordering = ["-start_date"]

    def __str__(self):
        return self.url.url


class Step(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    STEPS = (
        ("page_products", "page_products"),
        ("products_entities", "products_entities"),
        ("entities_classification", "entities_classification"),
        ("bad_url", "bad_url")
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="steps")
    step = models.CharField(max_length=25, choices=STEPS, default="page_products")
    time_started = models.DateTimeField(auto_now_add=True)
    time_submitted = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    step_data = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "steps"
        ordering = ["time_submitted"]

    def __str__(self):
        return f"{self.task.user.email} : {self.task.url} : {self.step}"

    def save(self, *args, **kwargs):
         
        #Convert all integers in step_data to strings
        if self.step_data:
            self.step_data = self._normalize_data(self.step_data)
            
        super(Step, self).save(*args, **kwargs) #proceed to save

    def _normalize_data(self, data):
        """
        A hacky fix for step 2 chrome extension bug.
        All integer values are expected to return as strings as converted by dynamo.
        To maintain that feature, we loop recursively through the step_data and convert all
        integers to strings before saving. This can be discarded when the chrome extension
        starts providing strings directly.
        """
        if isinstance(data, dict):
            dict_copy = data.copy()  #Used as iterator to avoid the 'DictionaryHasChanged' error
            for key, value in dict_copy.items():
                #booleans evaluate as integers too but we're not interested in booleans
                if isinstance(value, int) and not isinstance(value, bool):
                    data[key] = str(value)

                if isinstance(value, list):
                    data[key] = [self._normalize_data(v) for v in value]
                    
                if isinstance(value, dict):
                    self._normalize_data(value)
        return data


    @property
    def next_step(self):
        next_ = {
            "page_products": "products_entities",
            "products_entities": "entities_classification",
            "entities_classification": None,
            "bad_url": None
        }
        return next_[self.step]

class IntentData(TimestampModel):
    url = models.ForeignKey(Url, blank=False, null=False, on_delete=models.CASCADE, related_name="intent_data")
    department = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    subset = models.CharField(max_length=100, blank=True, null=True)
    intent = models.IntegerField()
    date_processed = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "intent_data"
        verbose_name_plural = "Intent Data"
        ordering = ["-date_processed"] #Newly processed first
    
    def __str__(self):
        levels = self.department, self.category, self.subcategory, self.subset
        return "|".join([level for level in levels if level])


class FacetProperty(TimestampModel):
    FACET_TYPES = (
        ("default", "default"),
        ("annotated", "annotated")
    )
    entity = models.ForeignKey(IntentData, blank=False, null=True, on_delete=models.CASCADE, related_name="facet_properties")
    facet = models.CharField(max_length=100)
    facet_type = models.CharField(max_length=10, choices=FACET_TYPES)
    entity_intent = models.IntegerField()
    facet_intent = models.IntegerField()

    class Meta:
        verbose_name_plural = "Facet properties"
        db_table = "facet_properties"

class SelectedProduct(TimestampModel):
    entity = models.ForeignKey(IntentData, blank=False, null=True, on_delete=models.CASCADE, related_name="selected_products")
    product = models.CharField(max_length=100)
    intent = models.IntegerField()


class AnnotationStats(User):
    """
    Not an actual model, Django doesn't allow registering a single model more than once
    so we use this as a proxy so we can add annotation statistics to the admin site
    """
    class Meta:
        proxy = True
        verbose_name_plural = "Annotation Scoreboard"


class TBAQ(Url):
    "Proxy model to show urls in queue"

    class Meta:
        proxy = True
        verbose_name = "Url"
        verbose_name_plural = "TBAQ"

class RawUrl(Url):
    "Proxy model to show urls that has not been decided upon"

    class Meta:
        proxy = True
        verbose_name_plural = "Raw URLs"

class SkippedUrl(Task):
    "Proxy model to show urls that are skipped"

    class Meta:
        proxy = True
        verbose_name = "Skipped Url"
        verbose_name_plural = "Skipped Urls"


class ArchiveQueue(Url):
    "Proxy model to show urls that are greenlisted but yet to be archived"

    class Meta:
        proxy = True
        verbose_name = "Url"
        verbose_name_plural = "Archive Queue"


class KnownUrls(Url):
    "Proxy model to show known urls"

    class Meta:
        proxy = True
        verbose_name = "Url"
        verbose_name_plural = "Known Urls"

class TaskBreakdown(Task):
    "Proxy model to show known urls"

    class Meta:
        proxy = True


def reset_url_to_default(sender, instance, **kwargs):
    # this function receives a signal to decrease the number of 
    # annotators working on a particular Url by 1 and restore Known  
    # back to False whenever a Task is deleted
    if instance.mode == "annotator":
        instance.url.known = False
        instance.url.annotators_assigned -= 1
        instance.url.save()

post_delete.connect(reset_url_to_default, sender=Task) 


class AnnotatorQueue(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content_object.name


class Country(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    urls = models.ManyToManyField(Url, blank=True, through='QueueUrlRelationship')
    annotator_queue = GenericRelation(AnnotatorQueue, related_query_name='countries')

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

class Client(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    name = models.CharField(max_length=100)
    urls = models.ManyToManyField(Url, blank=True, through='QueueUrlRelationship')
    annotator_queue = GenericRelation(AnnotatorQueue, related_query_name='clients')
    domains = models.ManyToManyField("annotation.DomainPriority", blank=True, through='ClientDomainRelationship')
    beeswax_list = models.ForeignKey("annotation.BeeswaxList", on_delete=models.SET_NULL, blank=True, null=True)
    domain_name = models.CharField(max_length=100, blank=True)
    bigquery_table = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class PageView(TimestampModel):
    number_of_views = models.PositiveIntegerField()
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.number_of_views)
    

class QueueUrlRelationship(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    client = models.ForeignKey("annotation.Client", on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey("annotation.Country", on_delete=models.CASCADE, blank=True, null=True)
    url = models.ForeignKey("annotation.Url", on_delete=models.CASCADE)
    events = models.CharField(max_length=50)
    page_views = models.ManyToManyField(PageView, blank=True)

    def __str__(self):
        return self.client.name if self.client else self.country.name

class ClientDomainRelationship(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    client = models.ForeignKey("annotation.Client", on_delete=models.CASCADE, null=True)
    domain = models.ForeignKey("annotation.DomainPriority", on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, choices=DomainPriority.STATUSES, default='amber')

    # def __str__(self):
    #     return f'{self.client} - {self.domain} - {self.status}'
    
@receiver(post_save, sender=Country)
def create_country_queue(sender, instance, created, **kwargs):
    if created:
        AnnotatorQueue.objects.create(
            content_type = ContentType.objects.get_for_model(instance),
            object_id = instance.id
        )

@receiver(post_save, sender=Client)
def create_client_queue(sender, instance, created, **kwargs):
    if created:
        AnnotatorQueue.objects.create(
            content_type = ContentType.objects.get_for_model(instance),
            object_id = instance.id
        )



class BeeswaxList(TimestampModel):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    name = models.CharField(max_length=50)
    redlist_id = models.IntegerField(null=True, blank=True)
    greenlist_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class UrlEditor(Url):
    class Meta:
        proxy = True
        verbose_name_plural = "URL Editor"


class ExtensionVersion(TimestampModel):
    version = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


class DomainLog(TimestampModel): 
    created = models.DateField(auto_now = True)

class NewTBAQ(QueueUrlRelationship):
    """
    Not an actual model, Django doesn't allow registering a single model more than once
    so we use this as a proxy so we can create a new tbaq on the admin site
    """
    class Meta:
        proxy = True
        verbose_name_plural = "New TBAQ"


class DomainOverview(ClientDomainRelationship):
    class Meta:
        proxy = True
        verbose_name_plural = "Domain Overview"

class Product(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=250)
    xpath = models.CharField(max_length=250)
    intent = models.IntegerField()

    def __str__(self):
        return str(self.product_id)


class EntityFacetRelationship(models.Model):
    FACET_CHOICES = (
        ('yes', 'yes'),
        ('no', 'no'),
        ('maybe', 'maybe'),
        
    )
    facet = models.ForeignKey('classification.FacetValue', on_delete=models.CASCADE)
    entity = models.ForeignKey('annotation.Entity', on_delete=models.CASCADE)
    has_facet = models.CharField(max_length=10, choices=FACET_CHOICES, default='maybe')


class Entity(models.Model):
    products = models.ManyToManyField('annotation.Product')
    avg_intent = models.IntegerField()
    classification = models.ManyToManyField('classification.Node')
    facets = models.ManyToManyField(FacetValue, blank=True, through='annotation.EntityFacetRelationship')

    class Meta:
        verbose_name_plural = 'Entities'

    def __str__(self):
        return self.avg_intent