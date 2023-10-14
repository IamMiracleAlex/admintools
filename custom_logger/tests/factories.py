import factory
import faker

fake = faker.Faker()


class RequestLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'custom_logger.RequestLog'

    duration = factory.Sequence(lambda n: int(n))
    user = factory.SubFactory('users.tests.factories.UserFactory')
    request_url = factory.Faker('url')
    request_body = factory.Faker('text')
    response_body = factory.Faker('text')
    request_method = factory.Iterator(['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
    response_status = factory.Iterator([200, 201, 302, 400, 403, 404, 500])


class ChromeExtensionLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'custom_logger.ChromeExtensionLog'

    user = factory.SubFactory('users.tests.factories.UserFactory')
    traceback = factory.Faker('text')
    local_storage = factory.Iterator([{fake.name(): fake.address()} for i in range(10) ])
    meta_info = factory.Faker('text')
