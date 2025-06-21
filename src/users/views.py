# src/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages # Dùng để hiển thị thông báo


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
