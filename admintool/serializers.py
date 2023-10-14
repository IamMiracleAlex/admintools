from rest_framework import serializers

from admintool.models import DataStatus


class DataStatusSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = DataStatus