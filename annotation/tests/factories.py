from django.utils import timezone

import factory

from annotation.models import Url, DomainPriority, FacetProperty


class UrlFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.Url'

    url = factory.Sequence(lambda n: 'https://centricityinsights.com/{}/'.format(n))
    page_views = factory.Sequence(lambda n: int(n))    
    last_counted = factory.LazyFunction(timezone.now)
    events = factory.Sequence(lambda n: int(n))
    annotators_assigned = 1
    required_annotations = 2
    archived_url = factory.Sequence(lambda n: 'https://archive/centricityinsights.com/{}/'.format(n))
    status = factory.Iterator([x[0] for x in DomainPriority.STATUSES])
    priority = factory.Iterator([x[0] for x in Url.PRIORITIES])
    domain = None
    known = True


class DomainPriorityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.DomainPriority'

    domain = factory.Sequence(lambda n: 'https://centricityinsights.com/{}/'.format(n))
    approximate_urls = factory.Sequence(lambda n: int(n))
    views = factory.Sequence(lambda n: int(n))
    last_counted = factory.LazyFunction(timezone.now)
    status = factory.Iterator([x[0] for x in DomainPriority.STATUSES])
    

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.Task'

    user = factory.SubFactory('users.tests.factories.UserFactory')
    date_completed = factory.LazyFunction(timezone.now)
    url = factory.SubFactory('annotation.tests.factories.UrlFactory')


class StepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.Step'

    task = factory.SubFactory('annotation.tests.factories.TaskFactory')
    step = "page_products"
    step_data = {'data': 'data'}


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.Country'

    name = "United States"
    short_name= "U.S"


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.Client'

    name = factory.Faker('name')


class RawUrlFactory(UrlFactory):
    class Meta:
        model = 'annotation.RawUrl'

    status='amber'

class IntentDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "annotation.IntentData"
    url = factory.SubFactory('annotation.tests.factories.UrlFactory')
    department = factory.Sequence(lambda n: 'Department {}'.format(n))
    category = factory.Sequence(lambda n: 'Category {}'.format(n))
    subcategory = factory.Sequence(lambda n: 'Subcategory {}'.format(n))
    subset = factory.Sequence(lambda n: 'Subset {}'.format(n))
    intent = factory.Sequence(lambda n: int(n))


class KnownUrlFactory(UrlFactory):
    class Meta:
        model = 'annotation.KnownUrls'

    known = True    


class TBAQFactory(UrlFactory):
    class Meta:
        model = 'annotation.TBAQ'

    status = "green"
    known = False


class ArchiveQueueFactory(UrlFactory):
    class Meta:
        model = 'annotation.ArchiveQueue'

    archived_url = ""
    status = 'green'


class PageViewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "annotation.PageView"

    number_of_views = factory.Sequence(lambda n: int(n))
    date = factory.LazyFunction(timezone.now)


class QueueUrlRelationshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.QueueUrlRelationship'

    client = factory.SubFactory('annotation.tests.factories.ClientFactory')
    country = factory.SubFactory('annotation.tests.factories.CountryFactory')
    url = factory.SubFactory('annotation.tests.factories.UrlFactory')
    events = factory.Sequence(lambda n: int(n))
    page_views = factory.RelatedFactory(PageViewFactory)

class BeeswaxListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.BeeswaxList'

    name =  factory.Faker('name')
    redlist_id = factory.Sequence(lambda n: int(n))
    greenlist_id = factory.Sequence(lambda n: int(n))


class ClientDomainRelationshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.ClientDomainRelationship'

    client = factory.SubFactory('annotation.tests.factories.ClientFactory')
    domain = factory.SubFactory('annotation.tests.factories.DomainPriorityFactory')
    status = factory.Iterator([x[0] for x in DomainPriority.STATUSES])


class FacetPropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.FacetProperty'

    entity = factory.SubFactory('annotation.tests.factories.IntentDataFactory')
    facet = factory.Faker('name')
    facet_type = factory.Iterator([x[0] for x in FacetProperty.FACET_TYPES])
    entity_intent = factory.Sequence(lambda n: int(n))
    facet_intent = factory.Sequence(lambda n: int(n))


class UrlEditorFactory(UrlFactory):
    class Meta:
        model = 'annotation.UrlEditor'


class UrlScrapedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.UrlScraped'

    text = factory.Faker('text')
    url = factory.Sequence(lambda n: int(n))
    instance_score = factory.Sequence(lambda n: int(n))
    original_text = factory.Faker('text')   


class ExtensionVersionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.ExtensionVersion'

    version =  factory.Sequence(lambda n: '{}.{}.{}'.format(n, n, n))


class TaskBreakdownFactory(TaskFactory):
    class Meta:
        model = 'annotation.TaskBreakdown'

    state = "completed" 
    mode = "annotator"
    completed = True

class DomainLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'annotation.DomainLog'


class NewTBAQFactory(QueueUrlRelationshipFactory):
    class Meta:
        model = 'annotation.NewTBAQ'


class BadUrlsFactory(TaskFactory):
    class Meta:
        model = 'annotation.SkippedUrl'