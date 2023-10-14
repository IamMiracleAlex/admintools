from django.db import models
from users.models import User


class BulkEdit(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    rows_affected = models.PositiveIntegerField()


class FacetBulkEdit(BulkEdit):
    class Meta:
        proxy = True
        verbose_name_plural = 'Facet Bulk Edit'


class DataRelease(models.Model):

    RESULTS = (
        ("success", "success"),
        ("failed", "failed")
    )

    last_run = models.DateTimeField(null=True)
    result = models.CharField(choices=RESULTS, null=True, max_length=10)