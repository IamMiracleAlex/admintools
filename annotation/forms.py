from django import forms
from django.core.exceptions import ValidationError

from annotation.models import ClientDomainRelationship


class ClientDomainRelationshipAdminForm(forms.ModelForm):
    
    class Meta:
        model = ClientDomainRelationship
        fields = '__all__'

    def clean(self):
 
        cleaned_data = super().clean()

        client = cleaned_data.get("client")
        domain = cleaned_data.get("domain")
        status = cleaned_data.get("status")

        if self.Meta.model.objects.filter(client=client, domain=domain, status=status).exists():

            # Do not redlist/amberlist/greenlist a domain, for thesame client multiple times
            raise ValidationError(
                f"You can NOT {status}list a domain for the same client multiple times."
            )

        
        if self.Meta.model.objects.filter(client=client, domain=domain, status__in=['red', 'amber', 'green']).exists():

            # Do not create another relationship for thesame client and domain
            raise ValidationError(
                f"A relationship already exists for this domain and client, please update it"
            )  
