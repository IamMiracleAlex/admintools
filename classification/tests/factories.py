import factory

from classification.models import FacetCategory, Node, NodeFacetRelationship


class FacetCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'classification.FacetCategory'

    title = factory.Sequence(lambda n: 'Facet Category Title {}'.format(n))
    description = factory.Sequence(lambda n: 'description {}'.format(n))
    facet_type = factory.Iterator([x[0] for x in FacetCategory.FACET_TYPE])


class FacetValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'classification.FacetValue'

    category = factory.SubFactory('classification.tests.factories.FacetCategoryFactory')
    label = factory.Sequence(lambda n: 'Facet Value Label {}'.format(n))
    description = factory.Sequence(lambda n: 'Facet Value Description {}'.format(n))


class NodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'classification.Node'

    title = factory.Sequence(lambda n: 'Node title {}'.format(n))
    description = factory.Sequence(lambda n: 'Node Description {}'.format(n))
    parent = None
    facets = factory.RelatedFactory(FacetValueFactory)


class NodeFacetRelationshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'classification.NodeFacetRelationship'

    node = factory.SubFactory('classification.tests.factories.NodeFactory')
    facet = factory.SubFactory('classification.tests.factories.FacetValueFactory')
    # has_facet = "sometimes"
    has_facet = factory.Iterator([x[0] for x in NodeFacetRelationship.OPTIONS])


class TaxonomyEditorFactory(NodeFactory):
    class Meta:
        model = 'classification.TaxonomyEditor'


class DeletedNodeFactory(NodeFactory):
    class Meta:
        model = 'classification.DeletedNode'
