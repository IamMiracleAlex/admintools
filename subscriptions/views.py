from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics
from .permissions import ClientPermission
from django.contrib.auth import get_user_model
from annotation.models import Client
from .models import Subscription
from .serializers import SubscriptionSerializer, DagSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
 

User = get_user_model()

# Create your views here.
class SubscriptionView(viewsets.ViewSet):
    permission_classes = [ClientPermission]

    # fetches the client object
    def get_object(self):
        obj = get_object_or_404(Client, pk=self.kwargs["client_id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, **kwargs):
        """
        status are query params -- SubCategory Statuses seperated by commas
        """
        if self.request.query_params.get("status"):
            query_status = self.request.query_params.get("status")
            try:
                client = self.get_object()
                query_set = Subscription.objects.filter(
                    status__in=query_status.split(","), client=client
                )
                serializer = SubscriptionSerializer(query_set, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Client.DoesNotExist:
                return  Response(
                    {"error": "Invalid Client ID"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {"error": "Status not valid"}, status=status.HTTP_400_BAD_REQUEST
        )


    def create(self, request, **kwargs):
        client = self.get_object()
        serializer = SubscriptionSerializer(
            data=request.data, context={"request": request, "client": client}, many=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


    @action(detail=False, methods=["patch"])
    def bulk_update(self, request, **kwargs):
        client = self.get_object()

        serializer = SubscriptionSerializer(
            data=request.data, many=True, partial=True
        )

        if  serializer.is_valid(raise_exception=True):
            for obj in serializer.data:
                try:
                    sub_object = Subscription.objects.get(
                        subcategory_id=obj["subcategory_id"], client=client
                    )
                    sub_object.status = obj["status"]
                    sub_object.save()
                except Subscription.DoesNotExist:
                    return Response(
                        {"detail": "Subscription_id not valid"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            return Response(
                {"success": "Subscriptions Updated"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "invalid input"}, status=status.HTTP_400_BAD_REQUEST
            )

            


class DagView(generics.ListAPIView):
    serializer_class = DagSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all().filter(status="approved").order_by('id')
    permission_classes = [IsAuthenticated, IsAdminUser]

