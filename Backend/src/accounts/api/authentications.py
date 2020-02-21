from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import ugettext_lazy as _
import datetime

EXPIRE_TIME = 5  # in minute


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

            # This is required for the time comparison
        now = timezone.now()

        if token.created < now - datetime.timedelta(minutes=EXPIRE_TIME):
            token.delete()
            raise AuthenticationFailed('Token has expired')

        return token.user, token
