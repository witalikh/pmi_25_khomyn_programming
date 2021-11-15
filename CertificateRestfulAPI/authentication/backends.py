from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom backend for authentication with JWT Tokens
    """

    # prefix before every Token
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
        Method for endpoints to authenticate with jwt-tokens
        """
        request.user = None

        # decompose header content
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        # nothing in header
        if not auth_header:
            return None

        # not enough args
        if len(auth_header) == 1:
            return None

        # a lot of args
        elif len(auth_header) > 2:
            return None

        else:
            # split decomposed header content into vars
            prefix = auth_header[0].decode('utf-8')
            token = auth_header[1].decode('utf-8')

            # check prefix
            if prefix.lower() != auth_header_prefix:
                return None

            return self._validate_token(request, token)

    def _validate_token(self, request, token):
        """
        Private method for checking token's validity
        """
        # decode token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

        except Exception:
            raise exceptions.AuthenticationFailed(
                "Authentication is non-performable on this token.")

        # find user
        try:
            user = User.objects.get(id=payload['id'])

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                "Cannot identify any user by this token."
            )

        return user, token
