from rest_framework import status
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response


from .serializers import (
    IntentSerializer,
    IntentChangeSerializer,
    CorrelationSerializer,
    CorrelationChangeSerializer,
    SalesSerializer,
    SalesChangeSerializer,
    PeriodSerializer,
)
from .serializers import IntentSerializer
from .models import (
    Intent,
    IntentChange,
    Correlation,
    CorrelationChange,
    Sales,
    SalesChange,
    Period,
)
from .permissions import IsClientAdminPermission
from annotation.models import Client
from users.models import ClientUser
from django.contrib.auth import get_user_model
from users.models import ClientUser

User = get_user_model()


class PriorityActionView(APIView):
    """Base view for all our views can inherit form"""

    permission_classes = (IsClientAdminPermission,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, *args, **kwargs):
        obj = self.model.objects.first()
        if not obj:
            user = User.objects.get(email=request.user.email)
            client_user = ClientUser.objects.get(user=user)
            client = Client.objects.get(clientuser__client=client_user.client)
            obj = self.model.objects.create(organization=client)
        serializer = self.serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        obj = self.model.objects.first()
        serializer = self.serializer(obj, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class IntentView(PriorityActionView):
    model = Intent
    serializer = IntentSerializer


class IntentChangeView(PriorityActionView):
    model = IntentChange
    serializer = IntentChangeSerializer


class CorrelationView(PriorityActionView):
    model = Correlation
    serializer = CorrelationSerializer


class CorrelationChangeView(PriorityActionView):
    model = CorrelationChange
    serializer = CorrelationChangeSerializer


class SalesView(PriorityActionView):
    model = Sales
    serializer = SalesSerializer


class SalesChangeView(PriorityActionView):
    model = SalesChange
    serializer = SalesChangeSerializer


class PeriodView(PriorityActionView):
    model = Period
    serializer = PeriodSerializer
