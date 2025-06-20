# Tệp định tuyến chính của ứng dụng QLthuvien <frameword Django>
from django.contrib import admin
from django.urls import path, include
from src.core.views import index_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),# Đường dẫn đến trang quản trị admin của Django
    path('', index_view, name='index'),# Trang chủ của ứng dụng, sẽ hiển thị trang index_view
    path('library/', include('src.library.urls')),# Bao gồm các URL của ứng dụng library
    path('accounts/', include('src.users.urls')), # bao gồm các URL của ứng dụng users
    # Đường dẫntự động tải lại trang khi có thay đổi trong mã nguồn
    path("__reload__/", include("django_browser_reload.urls")),
]

# Cấu hình để phục vụ static files trong môi trường development
if settings.DEBUG:# Kiểm tra xem ứng dụng có đang chạy trong chế độ DEBUG hay không
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)