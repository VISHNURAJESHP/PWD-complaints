import jwt
from rest_framework.exceptions import AuthenticationFailed
from User.models import User, official
from django.conf import settings

def authenticate_user(token):
    if not token:
        raise AuthenticationFailed('User is not authenticated')

    try:
        secret_key = settings.HASH_KEY
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload['id']
        user = User.objects.get(id=user_id)
        if not user:
            try:
                Official = official.objects.get(id=user_id)
                return Official
            except Official.DoesNotExist:
                raise AuthenticationFailed('user not found')
        else:
            return user
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('User token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
    except User.DoesNotExist:
        raise AuthenticationFailed('user not found')