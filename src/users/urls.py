# src/users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'), # URL cho trang đăng ký
    path('login/', views.login_view, name='login'),         # URL cho trang đăng nhập
    path('logout/', views.logout_view, name='logout'),       # URL cho chức năng đăng xuất
]
