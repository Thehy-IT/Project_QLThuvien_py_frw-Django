from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Min, Max
from .models import Book, Member, BorrowRecord
from django.db import transaction


# Định nghĩa các Form (có thể di chuyển sang tệp forms.py riêng nếu dự án lớn hơn)

# Form cho mô hình Book
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__' # Bao gồm tất cả các trường từ mô hình Book

# Form cho mô hình Member
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__' # Bao gồm tất cả các trường từ mô hình Member

# Form cho mô hình BorrowRecord
class BorrowRecordForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'member', 'due_date'] # Chỉ bao gồm các trường cần thiết cho việc mượn

# Form cho việc trả sách
class ReturnBookForm(forms.Form):
    borrow_record = forms.ModelChoiceField(
        queryset=BorrowRecord.objects.filter(return_date__isnull=True).order_by('member__name', 'book__title'),
        label="Chọn lượt mượn để trả",
        empty_label="-- Chọn sách và người mượn --",
        widget=forms.Select(attrs={'class': 'block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tùy chỉnh cách hiển thị cho mỗi lựa chọn trong danh sách
        self.fields['borrow_record'].label_from_instance = lambda obj: f"{obj.book.title} - (Mượn bởi: {obj.member.name})"

# New index view for dashboard
@login_required # Thêm decorator này để yêu cầu đăng nhập
def index(request):
    # Tính tổng số sách
    total_books = Book.objects.count()

    # Tính số sách đã mượn (trạng thái = 1)
    # Giả định rằng trạng thái sách được cập nhật chính xác thành 1 khi mượn
    borrowed_books = Book.objects.filter(status=1).count()

    # Tính số sách có sẵn (trạng thái = 0)
    # Giả định rằng trạng thái sách được cập nhật chính xác thành 0 khi trả
    available_books = Book.objects.filter(status=0).count()

    # Tính tổng số thành viên
    total_members = Member.objects.count()

    # Tính số sách quá hạn
    overdue_books_count = BorrowRecord.objects.filter(
        return_date__isnull=True,
        due_date__lt=timezone.now().date()
    ).count()

    context = {
        'total_books': total_books,
        'borrowed_books': borrowed_books,
        'available_books': available_books,
        'total_members': total_members,
        'overdue_books_count': overdue_books_count,
    }
    return render(request, 'index.html', context) # Giả định index.html nằm trong thư mục templates gốc của dự án

# Các View Quản lý Sách

# Hiển thị danh sách sách
def book_list(request):
    # Bắt đầu với tất cả sách, sắp xếp theo ID
    queryset = Book.objects.all().order_by('book_id')

    # Lấy các tham số lọc và tìm kiếm từ request.GET
    query = request.GET.get('q')
    status = request.GET.get('status')
    category = request.GET.get('category')
    author = request.GET.get('author')
    min_pages = request.GET.get('min_pages')
    max_pages = request.GET.get('max_pages')
    year = request.GET.get('year')

    # Áp dụng bộ lọc tìm kiếm nếu có
    if query:
        # Tìm kiếm trong cả title, author, và book_id
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(book_id__icontains=query)
        )
    
    # Áp dụng bộ lọc trạng thái nếu có (và không phải là chuỗi rỗng)
    if status:
        queryset = queryset.filter(status=status)
    
    # Áp dụng bộ lọc chủng loại nếu có (và không phải là chuỗi rỗng)
    if category:
        queryset = queryset.filter(category=category)

    # Lọc theo tác giả
    if author:
        queryset = queryset.filter(author=author)

    # Lọc theo khoảng số trang
    if min_pages:
        queryset = queryset.filter(pages__gte=min_pages)
    if max_pages:
        queryset = queryset.filter(pages__lte=max_pages)

    # Lọc theo năm sản xuất
    if year:
        queryset = queryset.filter(publication_year=year)

    # Lấy dữ liệu cho các bộ lọc trong modal
    category_choices = Book._meta.get_field('category').choices
    authors = Book.objects.values_list('author', flat=True).distinct().order_by('author')
    page_stats = Book.objects.aggregate(min=Min('pages'), max=Max('pages'))

    context = {
        'books': queryset, 
        'categories': category_choices,
        'authors': authors,
        'page_stats': page_stats,
    }
    return render(request, 'library/book_list.html', context)

# Tạo sách mới
def book_create(request):
    form = BookForm() # Khởi tạo form trống
    if request.method == 'POST': # Nếu yêu cầu là POST (người dùng gửi dữ liệu)
        form = BookForm(request.POST) # Điền dữ liệu từ request vào form
        if form.is_valid(): # Kiểm tra tính hợp lệ của form
            form.save() # Lưu sách mới vào cơ sở dữ liệu
            messages.success(request, "Sách đã được thêm thành công.")
            return redirect('book_list') # Chuyển hướng về trang danh sách sách
        else:
            messages.error(request, "Có lỗi xảy ra khi thêm sách.")
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Thêm'}) # Hiển thị form thêm sách

# Cập nhật thông tin sách

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk) # Lấy đối tượng sách dựa trên primary key (pk) hoặc trả về 404
    form = BookForm(instance=book) # Khởi tạo form với dữ liệu của sách hiện có
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book) # Cập nhật form với dữ liệu mới
        if form.is_valid():
            form.save() # Lưu thay đổi vào cơ sở dữ liệu
            messages.success(request, "Thông tin sách đã được cập nhật thành công.")
            return redirect('book_list')
        else:
            messages.error(request, "Có lỗi xảy ra khi cập nhật sách.")
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Sửa'}) # Hiển thị form sửa sách

# Xóa sách

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete() # Xóa sách khỏi cơ sở dữ liệu
        messages.success(request, "Sách đã được xóa thành công.")
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book}) # Hiển thị trang xác nhận xóa

# Tìm kiếm sách

def book_search(request):
    # Chuyển hướng logic tìm kiếm và lọc về view book_list để tránh trùng lặp code.
    # book_list giờ đây xử lý cả tìm kiếm và lọc.
    return book_list(request)


# Các View Quản lý Thành viên

# Hiển thị danh sách thành viên

def member_list(request):
    members = Member.objects.all()  # Lấy tất cả thành viên
    form = MemberForm()  # Tạo một instance của form để truyền cho modal
    context = {
        'members': members,
        'form': form,  # Thêm form vào context
    }
    return render(request, 'library/member_list.html', context)

# Tạo thành viên mới

def member_create(request):
    form = MemberForm()
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thành viên đã được thêm thành công.")
            return redirect('member_list')
        else:
            messages.error(request, "Có lỗi xảy ra khi thêm thành viên.")
    return render(request, 'library/member_form.html', {'form': form, 'action': 'Thêm'})

# Cập nhật thông tin thành viên

def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(instance=member)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Thông tin thành viên đã được cập nhật thành công.")
            return redirect('member_list')
        else:
            messages.error(request, "Có lỗi xảy ra khi cập nhật thành viên.")
    return render(request, 'library/member_form.html', {'form': form, 'action': 'Sửa'})

# Xóa thành viên

def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Thành viên đã được xóa thành công.")
        return redirect('member_list')
    return render(request, 'library/member_confirm_delete.html', {'member': member})

# Tìm kiếm thành viên

def member_search(request):
    query = request.GET.get('q')
    members = Member.objects.all() # Bắt đầu với tất cả thành viên
    if query:
        # Lọc thành viên theo tên hoặc ID thành viên
        members = members.filter(name__icontains=query) | \
                members.filter(member_id__icontains=query)
    
    form = MemberForm() # Cũng cần form cho trang kết quả tìm kiếm
    context = {
        'members': members, 'query': query, 'form': form
    }
    return render(request, 'library/member_list.html', context)


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
                messages.success(request, f"Sách '{book.title}' đã được mượn thành công bởi {borrow_record.member.name}.")
                return redirect('overdue_books') # Chuyển hướng đến trang sách quá hạn hoặc trang khác phù hợp
            else:
                form.add_error(None, "Sách này hiện không có sẵn để mượn.") # Thêm lỗi nếu sách không có sẵn
                messages.error(request, "Sách này hiện không có sẵn để mượn.")
        else:
            messages.error(request, "Có lỗi xảy ra khi tạo phiếu mượn.")
    return render(request, 'library/borrow_book.html', {'form': form}) # Hiển thị form mượn sách

# Hiển thị danh sách các cuốn sách đã mượn quá hạn

def overdue_books(request):
    # Lọc các bản ghi mượn mà chưa trả (return_date is null) và ngày hết hạn đã qua (due_date < ngày hiện tại)
    overdue_records = BorrowRecord.objects.filter(return_date__isnull=True, due_date__lt=timezone.now().date())
    return render(request, 'library/overdue_books.html', {'overdue_records': overdue_records}) # Hiển thị danh sách sách quá hạn

# View trả sách đã được hợp nhất và cải tiến
@transaction.atomic
def return_book(request):
    """
    Xử lý logic cho việc trả sách, sử dụng form để chọn lượt mượn.
    """
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            borrow_record = form.cleaned_data['borrow_record']
            
            # 1. Đánh dấu là đã trả sách bằng cách cập nhật ngày trả
            borrow_record.return_date = timezone.now()
            borrow_record.save()
            
            # 2. Cập nhật trạng thái sách thành "có sẵn" (status = 0) để thống nhất logic
            book = borrow_record.book
            book.status = 0
            book.save()
            
            messages.success(request, f"Đã trả sách '{book.title}' thành công!")
            return redirect('book_list') # Chuyển hướng về trang danh sách sách
    else:
        form = ReturnBookForm()

    # Nếu không có sách nào đang được mượn, hiển thị một thông báo thân thiện
    if not form.fields['borrow_record'].queryset.exists():
        messages.info(request, "Hiện tại không có sách nào đang được mượn để trả.")

    context = {
        'form': form,
        'page_title': 'Trả Sách' # Thêm tiêu đề cho trang
    }
    return render(request, 'library/return_book_form.html', context)
