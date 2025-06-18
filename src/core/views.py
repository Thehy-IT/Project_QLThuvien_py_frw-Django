from django.shortcuts import render

def index_view(request): # <-- Đảm bảo tên hàm là index_view
    return render(request, 'index.html')