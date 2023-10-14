from rest_framework import serializers
from .models import Subscription
from classification.serializers import NodeSerializer
from classification.models import Node
from users.models import ClientUser
from annotation.models import Country, Client


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("short_name", )


class SubscriptionSerializer(serializers.ModelSerializer):
    department = serializers.CharField(
        source='subcategory_id.parent.parent.title', read_only=True)

    category = serializers.CharField(
        source='subcategory_id.parent.title', read_only=True)

    subcategory = serializers.CharField(
        source='subcategory_id.title', read_only=True)

    class Meta:
        model = Subscription
        fields = ("subcategory_id", "status", "category",
                  "department", "subcategory")

    def create(self, validated_data):
        # this custom create function lets us change the status of an exisiting subscription
        # with a rejected or deleted status to inactive or create a new subscription if the
        # category doesnt exist
        subcategory_id = validated_data['subcategory_id']
        request = self.context["request"]
        client = self.context["client"]
        try:
            sub = Subscription.objects.get(
                subcategory_id=subcategory_id, client=client)
            if sub.status in ["rejected", "deleted"]:
                if request.user.is_superuser:
                    sub.status = "approved"
                else:
                    sub.status = "inactive"
                sub.save()
                return sub
            else:
                return sub
        except Subscription.DoesNotExist:
            status = "inactive"
            if request.user.is_superuser:
                status = "approved"
            return Subscription.objects.create(subcategory_id=subcategory_id, requester=request.user, client=client, status=status)


class DagSerializer(serializers.ModelSerializer):
    subcategory = serializers.CharField(
        source='subcategory_id.title', read_only=True)
    department = serializers.CharField(
        source='subcategory_id.parent.parent.title', read_only=True)
    bigquery_table = serializers.CharField(
        source='client.bigquery_table', read_only=True)
    countries = CountriesSerializer(read_only=True, many=True)

    class Meta:
        model = Subscription
        fields = ("subcategory", "department", "bigquery_table", "countries")
