from django.db import models
from django.utils import timezone

# Mô hình Book (Sách)
class Book(models.Model):
    # Các lựa chọn trạng thái của sách
    STATUS_CHOICES = [
        (0, 'Có sẵn'),
        (1, 'Đã mượn'),
        (2, 'Trạng thái khác'),
    ]

    # Các lựa chọn chủng loại sách
    CATEGORY_CHOICES = [
        ('TIEU_THUYET', 'Tiểu thuyết'),
        ('GIAO_KHOA', 'Giáo khoa'),
        ('KHOA_HOC', 'Khoa học'),
    ]

    book_id = models.CharField(max_length=20, unique=True, verbose_name="ID Sách") # ID của quyển sách, phải là duy nhất
    title = models.CharField(max_length=255, verbose_name="Tên Sách") # Tên sách
    author = models.CharField(max_length=255, verbose_name="Tác Giả") # Tác giả
    pages = models.IntegerField(verbose_name="Số Trang") # Số trang
    publication_year = models.IntegerField(verbose_name="Năm Xuất Bản") # Năm xuất bản
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="Trạng Thái Sách") # Trạng thái sách
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Chủng Loại Sách") # Chủng loại sách

    def __str__(self):
        # Hiển thị tên sách khi gọi đối tượng Book
        return self.title

    class Meta:
        verbose_name = "Sách"
        verbose_name_plural = "Sách"

# Mô hình Member (Thành viên)
class Member(models.Model):
    member_id = models.CharField(max_length=20, unique=True, verbose_name="ID Thành Viên") # ID thành viên, phải là duy nhất
    name = models.CharField(max_length=255, verbose_name="Tên Thành Viên") # Tên thành viên

    def __str__(self):
        # Hiển thị tên thành viên khi gọi đối tượng Member
        return self.name

    class Meta:
        verbose_name = "Thành viên"
        verbose_name_plural = "Thành viên"

# Mô hình BorrowRecord (Bản ghi mượn sách)
class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Sách") # Khóa ngoại đến mô hình Book
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name="Thành viên") # Khóa ngoại đến mô hình Member
    borrow_date = models.DateField(auto_now_add=True, verbose_name="Ngày Mượn") # Ngày mượn, tự động thêm khi tạo
    return_date = models.DateField(null=True, blank=True, verbose_name="Ngày Trả") # Ngày trả, có thể để trống
    due_date = models.DateField(verbose_name="Ngày Hết Hạn") # Ngày hết hạn trả sách

    def is_overdue(self):
        # Kiểm tra xem sách có quá hạn hay không
        # Quá hạn nếu chưa trả (return_date là null) và ngày hết hạn đã qua
        return self.return_date is None and self.due_date < timezone.now().date()

    def __str__(self):
        # Hiển thị thông tin bản ghi mượn
        return f"{self.member.name} đã mượn {self.book.title}"

    class Meta:
        verbose_name = "Bản ghi mượn"
        verbose_name_plural = "Bản ghi mượn"