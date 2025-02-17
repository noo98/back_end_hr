import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from .models import SystemUser  

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token["user_id"]

            user = SystemUser.objects.get(us_id=user_id)
            user.is_authenticated = True  # Manually set this attribute
        except (jwt.ExpiredSignatureError, jwt.DecodeError, SystemUser.DoesNotExist):
            raise AuthenticationFailed("Token ໃຊ້ງານບໍ່ໄດ້ ຫລື ຫມົດອາຍຸ")

        return (user, None)
