import factory


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'admintool.Status'


class DataStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'admintool.DataStatus'

    name = factory.Faker('name')
    value = factory.Sequence(lambda n: int(n)) 