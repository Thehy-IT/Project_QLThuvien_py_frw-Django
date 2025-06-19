# src/users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Form đăng ký người dùng tùy chỉnh
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Kế thừa các trường mặc định và thêm trường 'email'
        fields = UserCreationForm.Meta.fields + ('email',) 

# Form đăng nhập tùy chỉnh (có thể không cần chỉnh sửa nếu không có yêu cầu đặc biệt)
class CustomAuthenticationForm(AuthenticationForm):
    pass