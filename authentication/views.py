from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from .adapter import Google, register_client_user
from .serializers import GoogleAuthSerializer
from django.contrib.sites.shortcuts import get_current_site
from .utils import get_user_domain


class GoogleAuthView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GoogleAuthSerializer 

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializer.validated_data
            user_data = Google.validate(serializer['auth_token'])
            user_domain = get_user_domain(user_data["email"])
            user_data["user_domain"] = user_domain
            client_user_info = register_client_user(user_data)
            if not client_user_info :
                return Response({"message":"Unauthorized user"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(client_user_info, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)