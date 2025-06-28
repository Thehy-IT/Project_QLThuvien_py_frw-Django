from django import forms
from .models import Borrow

class ReturnBookForm(forms.Form):
    """
    Form để chọn một lượt mượn sách chưa được trả.
    """
    borrow_record = forms.ModelChoiceField(
        queryset=Borrow.objects.filter(return_date__isnull=True).order_by('member__name', 'book__title'),
        label="Chọn lượt mượn để trả",
        empty_label="-- Chọn sách và người mượn --",
        widget=forms.Select(attrs={'class': 'block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tùy chỉnh cách hiển thị cho mỗi lựa chọn trong danh sách, giúp người dùng dễ nhận biết hơn
        self.fields['borrow_record'].label_from_instance = lambda obj: f"{obj.book.title} - (Mượn bởi: {obj.member.name})"