from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from django.conf import settings
import jwt


class TokenUser:
    def __init__(self, payload):
        self.id               = payload.get('user_id')
        self.email            = payload.get('email', '')
        self.role             = payload.get('role', 'citizen')
        self.is_verified      = payload.get('is_verified', False)
        self.is_active        = True
        self.is_authenticated = True
        # ✅ Agrega estos
        self.is_staff         = payload.get('role') in ['admin', 'superadmin', 'staff']
        self.is_superuser     = payload.get('role') == 'superadmin'
        self.first_name       = payload.get('first_name', '')
        self.last_name        = payload.get('last_name', '')
        self.ci               = payload.get('ci', '')
        self.fecha_nacimiento = payload.get('fecha_nacimiento')  # 👈 AGREGAR

    def __str__(self):
        return self.email

    @property
    def is_anonymous(self):
        return False

    def has_perm(self, perm, obj=None):
        return self.role in ['admin', 'superadmin']

    def has_module_perms(self, app_label):
        return self.role in ['admin', 'superadmin']


class MicroserviceJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(
                token,
                settings.SIMPLE_JWT['SIGNING_KEY'],
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token inválido')

        return (TokenUser(payload), token)


class MicroserviceJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'certificates.authentication.MicroserviceJWTAuthentication'
    name         = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type':         'http',
            'scheme':       'bearer',
            'bearerFormat': 'JWT',
        }