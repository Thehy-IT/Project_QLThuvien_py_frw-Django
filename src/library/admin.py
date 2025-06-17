from django.contrib import admin
from .models import Book, Member, BorrowRecord

# Đăng ký mô hình Book vào trang quản trị Django
admin.site.register(Book)
# Đăng ký mô hình Member vào trang quản trị Django
admin.site.register(Member)
# Đăng ký mô hình BorrowRecord vào trang quản trị Django
admin.site.register(BorrowRecord)