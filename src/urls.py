"""
Tệp này định nghĩa định tuyến URL cho dự án Django.
URL configuration for QLthuvien project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from src.core import views as core_views # Import các view từ ứng dụng core

urlpatterns = [
    path("", core_views.index), # Trang chủ của ứng dụng
    path("admin/", admin.site.urls), # Đường dẫn đến trang quản trị Django
    path("library/", include("src.library.urls")), # Bao gồm các URL từ ứng dụng library
    path("__reload__/", include("django_browser_reload.urls")), # Dùng cho việc tải lại trình duyệt tự động khi phát triển
]

# Cấu hình phục vụ tệp media và static trong môi trường phát triển
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)