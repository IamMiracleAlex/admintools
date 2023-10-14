from rest_framework import serializers
from .models import (
    Intent,
    IntentChange,
    Correlation,
    CorrelationChange,
    Sales,
    SalesChange,
    Period,
)


class IntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intent
        fields = (
            "value",
            "value_operator",
            "period_operator",
            "status",
            "organization",
        )


class IntentChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentChange
        fields = (
            "value",
            "value_operator",
            "period_operator",
            "status",
            "organization",
        )


class CorrelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correlation
        fields = (
            "value",
            "value_operator",
            "period_operator",
            "status",
            "organization",
        )


class CorrelationChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrelationChange
        fields = (
            "value",
            "value_operator",
            "period_operator",
            "status",
            "organization",
        )


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = (
            "value",
            "value_operator",
            "period_operator",
            "status",
            "organization",
        )


class SalesChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesChange
        fields = (
            "value",
            "value_operator",
            "period_operator",
            "status",
            "organization",
        )


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ("period",)
