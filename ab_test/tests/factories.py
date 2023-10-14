import factory


class TestSetupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ab_test.TestSetup'


class TestInProgressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ab_test.TestInProgress'


class TestResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ab_test.TestResult'