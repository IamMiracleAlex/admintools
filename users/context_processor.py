from rest_framework.authtoken.models import Token
from django.conf import settings

def token_renderer(request):
   request_scheme = "http" if settings.ENVIRONMENT == "dev" else "https"
   if request.user.is_authenticated:
      return {
         'user_token': Token.objects.get_or_create(user=request.user)[0],
         'base_url': f'{request_scheme}://{request.get_host()}/'
      }
   else:
      return {}