"""
Tệp này cấu hình WSGI (Web Server Gateway Interface) cho dự án Django. Nó định nghĩa đối tượng application có thể gọi được cho các máy chủ web tương thích WSGI
WSGI config for QLthuvien project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QLthuvien.settings")

application = get_wsgi_application()
