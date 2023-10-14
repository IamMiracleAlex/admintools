from rest_framework import serializers
from annotation.models import Url

class ArchiveSerializer(serializers.Serializer):
    """
    Validate url submitted for archiving.
    Raise a validation error if it fails
    """
    url = serializers.CharField(required=True)
    archive = serializers.CharField(required=True)

    def validate_url(self, value):
        try:
            Url.objects.get(url=value)
            return value
        except:
            raise serializers.ValidationError("Url not found")
        
