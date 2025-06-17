"""Tệp này chứa các hàm xem (view functions) cho ứng dụng core"""
from django.shortcuts import render

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)
