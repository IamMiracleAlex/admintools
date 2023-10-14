from django.http import JsonResponse

from rest_framework import status

def custom_handler_500(request, *args, **kwargs):
    return JsonResponse({
            "detail":'An unexpected application error has occurred.',
            "code":'internal_server_error',
            "status":status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )