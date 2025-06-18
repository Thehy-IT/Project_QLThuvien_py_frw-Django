from django.contrib import admin
from django.urls import path, include
from src.core.views import index_view

# Để phục vụ các tệp tĩnh trong môi trường phát triển
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('library/', include('src.library.urls')), # Bao gồm các URL của ứng dụng thư viện

    # Thêm dòng này để django-browser-reload hoạt động
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)