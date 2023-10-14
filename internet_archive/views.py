from django.db.models import F, Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from .serializers import ArchiveSerializer
from annotation.models import Url
from internet_archive.models import ArchiveSetting

from drf_yasg.utils import swagger_auto_schema

class ArchiveView(APIView):
    """
    GET fetches the next url to be archived
    POST saves a fetched archive
    """
    parser_classes = [JSONParser]

    def get(self, request, **kwargs):

        tbaq = Url.objects.filter(status="green", known=False, archived_url="").order_by('archive_attempt_count')
        archive_setting = ArchiveSetting.objects.first()
        number_of_urls = archive_setting.number_of_urls

        if tbaq:
            urls = []
            for url in tbaq[:number_of_urls]:
                urls.append(url.url)
                url.archive_attempt_count += 1
                url.save()
            data = {
                "urls": urls,
                'settings': {
                    'method': archive_setting.archive_method,
                    'number_of_urls': number_of_urls,
                }
                }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({"details":"No url to archive at this time"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


    @swagger_auto_schema(request_body=ArchiveSerializer)
    def post(self, request, **kwargs):

        data = ArchiveSerializer(data=request.data)

        if data.is_valid(raise_exception=True):
            data = data.validated_data

            url = Url.objects.get(url=data['url'])
            url.archived_url = data['archive']
            url.save()

            return Response({"mesage":"Success"}, status=status.HTTP_200_OK)

