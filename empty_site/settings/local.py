from .base import *

SOCIAL_AUTH_VK_OAUTH2_KEY = '7471838'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'jJHhoDyuT5vIi7DC3W02'


DEBUG = True
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
