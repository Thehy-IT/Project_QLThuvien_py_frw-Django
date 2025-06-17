from django.urls import path
from . import views # Import các view từ tệp views.py cùng thư mục

urlpatterns = [
    # Các URL cho Sách
    path('books/', views.book_list, name='book_list'), # Danh sách sách
    path('books/add/', views.book_create, name='book_create'), # Thêm sách mới
    path('books/edit/<int:pk>/', views.book_update, name='book_update'), # Chỉnh sửa sách theo ID (pk)
    path('books/delete/<int:pk>/', views.book_delete, name='book_delete'), # Xóa sách theo ID (pk)
    path('books/search/', views.book_search, name='book_search'), # Tìm kiếm sách

    # Các URL cho Thành viên
    path('members/', views.member_list, name='member_list'), # Danh sách thành viên
    path('members/add/', views.member_create, name='member_create'), # Thêm thành viên mới
    path('members/edit/<int:pk>/', views.member_update, name='member_update'), # Chỉnh sửa thành viên theo ID (pk)
    path('members/delete/<int:pk>/', views.member_delete, name='member_delete'), # Xóa thành viên theo ID (pk)
    path('members/search/', views.member_search, name='member_search'), # Tìm kiếm thành viên

    # Các URL cho việc Mượn/Trả sách
    path('borrow/', views.borrow_book, name='borrow_book'), # Trang mượn sách
    path('return/<int:pk>/', views.return_book, name='return_book'), # Trả sách theo ID của bản ghi mượn (pk)
    path('overdue/', views.overdue_books, name='overdue_books'), # Danh sách sách quá hạn
]