from django.shortcuts import render # Dùng để render các template HTML
from src.library.models import Book, Member, BorrowRecord # Import các model từ ứng dụng 'library' để truy vấn dữ liệu
from django.utils import timezone # Import timezone để làm việc với ngày giờ, cần cho việc kiểm tra sách quá hạn

def index_view(request): # Định nghĩa hàm view cho trang chủ
    # Lấy tổng số sách hiện có trong thư viện
    # Book.objects.count() sẽ đếm tất cả các bản ghi trong bảng Book
    total_books = Book.objects.count()
    
    # Lấy số sách đang được mượn
    # Giả sử trạng thái sách '1' (hoặc một giá trị nào đó) biểu thị sách đang được mượn
    # Bạn cần đảm bảo trường 'status' trong model Book của bạn định nghĩa trạng thái này
    borrowed_books = Book.objects.filter(status=1).count()
    
    # Lấy tổng số thành viên của thư viện
    # Member.objects.count() sẽ đếm tất cả các bản ghi trong bảng Member
    total_members = Member.objects.count()
    
    # Lấy số lượt mượn sách quá hạn
    # Truy vấn BorrowRecord (bảng ghi mượn trả)
    # return_date__isnull=True: Lọc các bản ghi mà sách chưa được trả (return_date còn trống)
    # due_date__lt=timezone.now().date(): Lọc các bản ghi mà ngày đến hạn (due_date) đã qua ngày hiện tại
    overdue_books_count = BorrowRecord.objects.filter(
        return_date__isnull=True,
        due_date__lt=timezone.now().date()
    ).count()

    # Tạo một dictionary chứa tất cả các biến số liệu để truyền vào template
    context = {
        'total_books': total_books,
        'borrowed_books': borrowed_books,
        'total_members': total_members,
        'overdue_books_count': overdue_books_count,
    }
    
    # Render template 'index.html' và truyền dữ liệu trong 'context' vào đó
    return render(request, 'index.html', context)