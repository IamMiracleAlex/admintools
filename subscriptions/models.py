from django.db import models
from django.contrib.auth import get_user_model
from classification.models import Node
from annotation.models import Client, Country

User = get_user_model()

class Subscription(models.Model):
    STATUSES = (
        ("pending", "pending"),
        ("approved", "approved"),
        ("rejected", "rejected"),
        ("deleted", "deleted"),
        ("inactive", "inactive"),
    )

    requester = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(Node, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default="inactive", max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(Country, blank=True)

    class Meta:
        db_table = "subcriptions"

    def __str__(self):
        return str(self.id)
