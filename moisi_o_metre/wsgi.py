"""
WSGI config for moisi_o_metre project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from . import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moisi_o_metre.settings')

application = get_wsgi_application()
