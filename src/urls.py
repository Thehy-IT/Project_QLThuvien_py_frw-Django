# src/urls.py
from django.contrib import admin
from django.urls import path, include
from src.core.views import index_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('library/', include('src.library.urls')),
    path('accounts/', include('src.users.urls')), # Thêm dòng này để bao gồm các URL của ứng dụng users
    path("__reload__/", include("django_browser_reload.urls")),
]

# Cấu hình để phục vụ static files trong môi trường development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)