from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.utils import timezone
from .models import Book, Member, BorrowRecord

# Định nghĩa các Form (có thể di chuyển sang tệp forms.py riêng nếu dự án lớn hơn)

# Form cho mô hình Book
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__' # Bao gồm tất cả các trường từ mô hình Book

# Form cho mô hình Member
class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__' # Bao gồm tất cả các trường từ mô hình Member

# Form cho mô hình BorrowRecord
class BorrowRecordForm(ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'member', 'due_date'] # Chỉ bao gồm các trường cần thiết cho việc mượn


# Các View Quản lý Sách

# Hiển thị danh sách sách
def book_list(request):
    books = Book.objects.all() # Lấy tất cả sách từ cơ sở dữ liệu
    return render(request, 'library/book_list.html', {'books': books})

# Tạo sách mới
def book_create(request):
    form = BookForm() # Khởi tạo form trống
    if request.method == 'POST': # Nếu yêu cầu là POST (người dùng gửi dữ liệu)
        form = BookForm(request.POST) # Điền dữ liệu từ request vào form
        if form.is_valid(): # Kiểm tra tính hợp lệ của form
            form.save() # Lưu sách mới vào cơ sở dữ liệu
            return redirect('book_list') # Chuyển hướng về trang danh sách sách
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Thêm'}) # Hiển thị form thêm sách

# Cập nhật thông tin sách
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk) # Lấy đối tượng sách dựa trên primary key (pk) hoặc trả về 404
    form = BookForm(instance=book) # Khởi tạo form với dữ liệu của sách hiện có
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book) # Cập nhật form với dữ liệu mới
        if form.is_valid():
            form.save() # Lưu thay đổi vào cơ sở dữ liệu
            return redirect('book_list')
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Sửa'}) # Hiển thị form sửa sách

# Xóa sách
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete() # Xóa sách khỏi cơ sở dữ liệu
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book}) # Hiển thị trang xác nhận xóa

# Tìm kiếm sách
def book_search(request):
    query = request.GET.get('q') # Lấy chuỗi tìm kiếm từ tham số URL 'q'
    books = Book.objects.all() # Lấy tất cả sách ban đầu
    if query:
        # Lọc sách theo tiêu đề, tác giả hoặc ID sách (không phân biệt chữ hoa/thường)
        books = books.filter(title__icontains=query) | \
                  books.filter(author__icontains=query) | \
                  books.filter(book_id__icontains=query)
    return render(request, 'library/book_list.html', {'books': books, 'query': query}) # Hiển thị danh sách sách đã lọc


# Các View Quản lý Thành viên

# Hiển thị danh sách thành viên
def member_list(request):
    members = Member.objects.all() # Lấy tất cả thành viên
    return render(request, 'library/member_list.html', {'members': members})

# Tạo thành viên mới
def member_create(request):
    form = MemberForm()
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    return render(request, 'library/member_form.html', {'form': form, 'action': 'Thêm'})

# Cập nhật thông tin thành viên
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(instance=member)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    return render(request, 'library/member_form.html', {'form': form, 'action': 'Sửa'})

# Xóa thành viên
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('member_list')
    return render(request, 'library/member_confirm_delete.html', {'member': member})

# Tìm kiếm thành viên
def member_search(request):
    query = request.GET.get('q')
    members = Member.objects.all()
    if query:
        # Lọc thành viên theo tên hoặc ID thành viên
        members = members.filter(name__icontains=query) | \
                    members.filter(member_id__icontains=query)
    return render(request, 'library/member_list.html', {'members': members, 'query': query})


# Các View Quản lý Mượn/Trả Sách

# Mượn sách
def borrow_book(request):
    form = BorrowRecordForm() # Khởi tạo form mượn sách
    if request.method == 'POST':
        form = BorrowRecordForm(request.POST)
        if form.is_valid():
            borrow_record = form.save(commit=False) # Không lưu ngay lập tức để chỉnh sửa trạng thái sách
            book = borrow_record.book
            if book.status == 0:  # Kiểm tra nếu sách có sẵn (status = 0)
                book.status = 1  # Đặt trạng thái sách thành "đã mượn"
                book.save()
                borrow_record.save() # Lưu bản ghi mượn
                return redirect('overdue_books') # Chuyển hướng đến trang sách quá hạn hoặc trang khác phù hợp
            else:
                form.add_error(None, "Sách này hiện không có sẵn để mượn.") # Thêm lỗi nếu sách không có sẵn
    return render(request, 'library/borrow_book.html', {'form': form}) # Hiển thị form mượn sách

# Trả sách
def return_book(request, pk):
    borrow_record = get_object_or_404(BorrowRecord, pk=pk) # Lấy bản ghi mượn dựa trên pk
    if request.method == 'POST':
        if borrow_record.return_date is None: # Chỉ xử lý nếu sách chưa được trả
            borrow_record.return_date = timezone.now().date() # Đặt ngày trả là ngày hiện tại
            borrow_record.book.status = 0  # Đặt trạng thái sách về "có sẵn"
            borrow_record.book.save()
            borrow_record.save()
        return redirect('overdue_books') # Chuyển hướng đến trang sách quá hạn hoặc danh sách sách đã mượn
    return render(request, 'library/return_book_confirm.html', {'borrow_record': borrow_record}) # Hiển thị trang xác nhận trả sách


# Hiển thị danh sách các cuốn sách đã mượn quá hạn
def overdue_books(request):
    # Lọc các bản ghi mượn mà chưa trả (return_date is null) và ngày hết hạn đã qua (due_date < ngày hiện tại)
    overdue_records = BorrowRecord.objects.filter(return_date__isnull=True, due_date__lt=timezone.now().date())
    return render(request, 'library/overdue_books.html', {'overdue_records': overdue_records}) # Hiển thị danh sách sách quá hạn