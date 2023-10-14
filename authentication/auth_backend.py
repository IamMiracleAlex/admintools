from django.contrib.auth.backends import ModelBackend
from users.models import User


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, request,  username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username) 
            if user.user_type != "client":
                return None
            if password:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
            else:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None