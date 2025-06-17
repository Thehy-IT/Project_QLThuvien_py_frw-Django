"""
ASGI config for QLthuvien project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
# định nghĩa đối tượng application có thể gọi được cho các máy chủ web tương thích ASGI.
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

application = get_asgi_application()
