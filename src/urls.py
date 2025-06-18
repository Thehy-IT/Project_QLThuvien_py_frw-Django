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
    path("__reload__/", include("django_browser_reload.urls")),
    
    # Thêm các URL xác thực của Django
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('src.users.urls')), # Thêm URL cho đăng ký
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)