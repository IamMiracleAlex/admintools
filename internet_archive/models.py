from django.db import models
from django.core.exceptions import ValidationError


class ArchiveSetting(models.Model):
    ArchiveChoices = (
        ('internal_tool', 'Internal Tool'),
        ('wayback_machine', 'WayBack Machine'),
        ('default', 'Default'),
    )
    archive_method = models.CharField(max_length=20, choices=ArchiveChoices, default='default')
    number_of_urls = models.PositiveIntegerField(default=15, help_text='Number urls to archive per request, max: 20')

    def clean(self):
        # Don't allow more than 20 urls per request
        if self.number_of_urls > 20:
            raise ValidationError('You may not set above 20 urls per request')
