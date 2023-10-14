import uuid, json
import boto3
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_jwt.settings import api_settings


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # The line below is a workaround for using social auth.
        # Sets a random password if user signs up via social auth
        pass_ = password if password else uuid.uuid4().hex 
        user.set_password(pass_)
        user.save()
        return user
        # I think the pipeline works

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # PROTECTED MODEL: DO NOT MODIFY, Please see the readme for more information

    TYPES = (
        ("developer","developer"),
        ("annotator", "annotator"),
        ("manager", "manager"),
        ("machine", "machine"),
         ("client", "client")
    )
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=12, choices=TYPES)
    queue = models.ForeignKey("annotation.AnnotatorQueue", on_delete=models.DO_NOTHING, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    @property
    def is_verified_for_ses(self):
        """
        Checks if a user is verified to receive email from amazon's ses
        returns bool
        """
        client = boto3.client('ses', region_name="us-east-1")
        response = client.list_identities(IdentityType='EmailAddress', MaxItems=999)
        registered_users = response["Identities"]

        return self.email in registered_users


    @property
    def looker_fields(self):
        return {
            'permissions' : json.dumps(['see_user_dashboards', 'see_lookml_dashboards', 'access_data', 'see_looks', 'download_with_limit', 'explore']),
            'models' : json.dumps(["User"]),
            'access_filters' : 'strings',
            'user_attributes' : 'strings',
            'group_ids' : 'strings',
            'external_group_id' : 'strings',
            'external_user_id' : json.dumps(self.pk)
        }
    
    @staticmethod
    def token(user):
        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        return jwt_token


class ClientUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    client = models.ForeignKey("annotation.Client", on_delete=models.DO_NOTHING, null=True, blank=True)
    is_admin = models.BooleanField(default=False)




@receiver(post_save, sender = User)
def create_client_user(sender, instance, created, **kwargs):
    if instance.user_type == "client":
        ClientUser.objects.get_or_create(user = instance)
    
    
