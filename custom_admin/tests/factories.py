import factory


class BulkEditFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'custom_admin.BulkEdit'

    user = factory.SubFactory('users.tests.factories.UserFactory')
    rows_affected = factory.Sequence(lambda n: int(n))


