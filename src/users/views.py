# src/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required # Dùng để bảo vệ các view chỉ cho người dùng đã đăng nhập
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages # Dùng để hiển thị thông báo
from django.contrib.auth.decorators import login_required # Import decorator này
from django.contrib import messages # Import messages để hiển thị thông báo


# View xử lý chức năng đăng ký
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Lưu người dùng mới vào database
            login(request, user) # Đăng nhập người dùng ngay sau khi đăng ký thành công
            messages.success(request, "Đăng ký tài khoản thành công!") # Hiển thị thông báo thành công
            return redirect('index') # Chuyển hướng về trang chủ
        else:
            # Nếu form không hợp lệ, duyệt qua các lỗi và hiển thị thông báo
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Lỗi ở trường '{field}': {error}")
    else:
        form = CustomUserCreationForm() # Tạo form rỗng cho lần truy cập đầu tiên
    return render(request, 'users/register.html', {'form': form})

# View xử lý chức năng đăng nhập
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Xác thực người dùng
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user) # Đăng nhập người dùng
                messages.success(request, f"Chào mừng trở lại, {username}!") # Hiển thị thông báo thành công
                return redirect('index') # Chuyển hướng về trang chủ
            else:
                messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.") # Thông báo lỗi nếu xác thực thất bại
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin đăng nhập.") # Thông báo lỗi chung nếu form không hợp lệ
    else:
        form = CustomAuthenticationForm() # Tạo form rỗng cho lần truy cập đầu tiên
    return render(request, 'users/login.html', {'form': form})

# View xử lý chức năng đăng xuất
def logout_view(request):
    logout(request) # Thực hiện đăng xuất người dùng
    messages.info(request, "Bạn đã đăng xuất khỏi hệ thống.") # Hiển thị thông báo đăng xuất
    return redirect('login') # Chuyển hướng về trang đăng nhập

# Các View Quản lý Sách

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def book_create(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sách đã được thêm thành công.")
            return redirect('book_list')
        else:
            messages.error(request, "Có lỗi xảy ra khi thêm sách.")
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Thêm'})

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(instance=book)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Thông tin sách đã được cập nhật thành công.")
            return redirect('book_list')
        else:
            messages.error(request, "Có lỗi xảy ra khi cập nhật sách.")
    return render(request, 'library/book_form.html', {'form': form, 'action': 'Sửa'})

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Sách đã được xóa thành công.")
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book})

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def book_search(request):
    query = request.GET.get('q')
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query) | \
                  books.filter(author__icontains=query) | \
                  books.filter(book_id__icontains=query)
    return render(request, 'library/book_list.html', {'books': books, 'query': query})


# Các View Quản lý Thành viên

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def member_list(request):
    members = Member.objects.all()
    return render(request, 'library/member_list.html', {'members': members})

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
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

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
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

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "Thành viên đã được xóa thành công.")
        return redirect('member_list')
    return render(request, 'library/member_confirm_delete.html', {'member': member})

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def member_search(request):
    query = request.GET.get('q')
    members = Member.objects.all()
    if query:
        members = members.filter(name__icontains=query) | \
                    members.filter(member_id__icontains=query)
    return render(request, 'library/member_list.html', {'members': members, 'query': query})


# Các View Quản lý Mượn/Trả Sách

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def borrow_book(request):
    form = BorrowRecordForm()
    if request.method == 'POST':
        form = BorrowRecordForm(request.POST)
        if form.is_valid():
            borrow_record = form.save(commit=False)
            book = borrow_record.book
            if book.status == 0: # 0 là trạng thái 'có sẵn'
                book.status = 1 # 1 là trạng thái 'đã mượn'
                book.save()
                borrow_record.save()
                messages.success(request, f"Sách '{book.title}' đã được mượn thành công bởi {borrow_record.member.name}.")
                return redirect('overdue_books')
            else:
                form.add_error(None, "Sách này hiện không có sẵn để mượn.")
                messages.error(request, "Sách này hiện không có sẵn để mượn.")
        else:
            messages.error(request, "Có lỗi xảy ra khi tạo phiếu mượn.")
    return render(request, 'library/borrow_book.html', {'form': form})

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def return_book(request, pk):
    borrow_record = get_object_or_404(BorrowRecord, pk=pk)
    if request.method == 'POST':
        if borrow_record.return_date is None: # Chỉ cập nhật nếu sách chưa được trả
            borrow_record.return_date = timezone.now().date()
            borrow_record.book.status = 0 # Đặt trạng thái sách về 'có sẵn'
            borrow_record.book.save()
            borrow_record.save()
            messages.success(request, f"Sách '{borrow_record.book.title}' đã được trả thành công.")
        else:
            messages.info(request, "Sách này đã được trả trước đó.")
        return redirect('overdue_books')
    return render(request, 'library/return_book_confirm.html', {'borrow_record': borrow_record})

@login_required # Chỉ cho phép người dùng đã đăng nhập truy cập
def overdue_books(request):
    # Lấy các phiếu mượn chưa trả và đã quá hạn
    overdue_records = BorrowRecord.objects.filter(return_date__isnull=True, due_date__lt=timezone.now().date())
    return render(request, 'library/overdue_books.html', {'overdue_records': overdue_records})
