from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from custom_logger.serializers import ChromeExtensionLogSerializer


class ChromeExtensionLogView(generics.CreateAPIView):
    '''Post chrome extension logs data'''

    permission_classes = [IsAuthenticated]
    serializer_class = ChromeExtensionLogSerializer