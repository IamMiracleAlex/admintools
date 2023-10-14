import os

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.utils import create_signed_url


class LookerAuth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        url = create_signed_url(embed_url="/embed/dashboards/3",
                                user=user,
                                host=settings.LOOKER_HOST, 
                                secret=settings.LOOKER_SECRET,)
        return Response({'url': url})        