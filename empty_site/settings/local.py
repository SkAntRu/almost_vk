from .base import *
from .other.secrets import SOCIAL_AUTH_VK_OAUTH2_KEY, SOCIAL_AUTH_VK_OAUTH2_SECRET, SECRET_KEY


DEBUG = True
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
