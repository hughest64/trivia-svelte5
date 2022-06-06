from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

import jwt

User = get_user_model()

class JwtAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('You need to log in!')

        try:
            # TODO: make an actual token variable
            payload = jwt.decode(
                token,
                settings.JWT_TOKEN_SECRET,
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('You need to log in!')

        
        # TODO: handle bad id? Is that possible at this point?
        # should we just return AnonymousUser?
        user = User.objects.get(id=payload['id'])

        return (user, None)