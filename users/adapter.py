from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from allauth.account.adapter import get_adapter as get_account_adapter
from users.models import User


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
   def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        You can use this hook to intervene, e.g. abort the login by
        raising an ImmediateHttpResponse

        """
        socialUser = sociallogin.user
        """
        This checks if a uid exists against this user, on first "login with google" the id is None
        and then it is set against this user object in database.
        """
        if socialUser.id:
        #if this is NOT NONE we return/end the function
            return
        # if previous statement was NONE we start executing code from here
        try:
            user = User.objects.get(email=socialUser.email)
            # if user exists then connect the existing account with social account and login
            sociallogin.state['process'] = 'connect'
            perform_login(request, user, 'none')
        except User.DoesNotExist:
            pass
        """I don't want to catch this exception at all, the logic means that this email
        does not exist in our dtabase so user is signing up for the first time
         It should continue to the next flow (handeled by allauth library) and call the save_user() method"""


   def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. In case of auto-signup,
        the signup form is not available.
        """
        socialUser = sociallogin.user
        socialUser.set_unusable_password()
        socialUser.is_staff = True
        socialUser.is_active = True
        """
        Refer allauth.socialaccount.form.py for details on below method
        saves the social user, token and else in allauth related table
        """
        sociallogin.save(request)
        return socialUser
