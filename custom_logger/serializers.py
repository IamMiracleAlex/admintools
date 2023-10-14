from rest_framework import serializers

from custom_logger.models import ChromeExtensionLog


class ChromeExtensionLogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ChromeExtensionLog

    def create(self, validated_data):
        user = self.context['request'].user  
        celog = self.Meta.model.objects.create(
            user=user, **validated_data
        )
        return celog
        