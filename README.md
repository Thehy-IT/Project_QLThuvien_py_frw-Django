# GitHub Codespaces ♥️ Django

Welcome to your shiny new Codespace running Django! We've got everything fired up and running for you to explore Django.

You've got a blank canvas to work on from a git perspective as well. There's a single initial commit with what you're seeing right now - where you go from here is up to you!

Everything you do here is contained within this one codespace. There is no repository on GitHub yet. If and when you’re ready you can click "Publish Branch" and we’ll create your repository and push up your project. If you were just exploring then and have no further need for this code then you can simply delete your codespace and it's gone forever.

# Đề bài: Xây dựng ứng dụng quản lý thư viện bằng Python

## Yêu cầu chung
- Sử dụng mô hình lập trình hướng đối tượng
- Kết nối với cơ sở dữ liệu
- Sử dụng framework Django

## Cấu trúc dữ liệu
### Sách
- ID của quyển sách
- Tên sách
- Tác giả
- Số trang
- Năm xuất bản
- Trạng thái sách (0: có sẵn, 1: đã mượn, 2: trạng thái khác)
- Chủng loại sách (Tiểu thuyết, Giáo khoa, Khoa học)

### Thành viên thư viện
- ID thành viên
- Tên thành viên

## Các tính năng ứng dụng
### Quản lý sách
- Thêm, xóa, sửa, tìm kiếm, hiển thị sách

### Quản lý thành viên
- Thêm, xóa, sửa, tìm kiếm, hiển thị thành viên

### Quản lý mượn sách
- Mượn sách, trả sách
- Hiển thị danh sách các cuốn sách đã mượn quá hạn (kèm thông tin người mượn)


## installing dependancies

```python
pip install -r requirements.txt
```

## To collect static files:

```python
python manage.py collectstatic
```

## To run this application:

```python
python manage.py runserver
```
