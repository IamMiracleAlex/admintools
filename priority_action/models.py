from django.db import models
from annotation.models import Client


class PriorityAction(models.Model):
    """
    This is our base model, since the value field is the only peculiar field
    across all models
    """

    VALUE_OPERATORS = (
        (">", ">"),
        (">=", ">="),
        ("=", "="),
        ("<", "<"),
        ("<=", "<="),
    )

    PERIOD_OPERATORS = (("sum", "sum"), ("average", "average"), ("max", "max"))

    value_operator = models.CharField(
        choices=VALUE_OPERATORS, default="=", max_length=2
    )
    period_operator = models.CharField(
        choices=PERIOD_OPERATORS, default="sum", max_length=10
    )
    status = models.BooleanField(default=False)
    organization = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False)


class Intent(PriorityAction):
    value = models.IntegerField(default=0)


class IntentChange(PriorityAction):
    value = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Correlation(PriorityAction):
    value = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)


class CorrelationChange(PriorityAction):
    value = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Sales(PriorityAction):
    value = models.IntegerField(default=0)


class SalesChange(PriorityAction):
    value = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


class Period(models.Model):
    period = models.PositiveIntegerField(default=0)
