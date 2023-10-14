import factory

from internet_archive.models import ArchiveSetting


class ArchiveSettingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'internet_archive.ArchiveSetting'

    archive_method = factory.Iterator([x[0] for x in  ArchiveSetting.ArchiveChoices])
    number_of_urls = factory.Sequence(lambda n: int(n))
