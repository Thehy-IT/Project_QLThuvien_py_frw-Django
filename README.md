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

# Hướng dẫn RunApp
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
## Thực hiện bởi:
- Sinh viên: Huỳnh Thế Hy
- Năm học: 2024-2025 <năm 2>

## Phần cần phát triển thêm
- Cải thiện giao diện người dùng:
    + tạo giao diện đăng nhập/đăng ký.
    + trực quan hóa biểu đồ thống kê sách, thành viên riêng.
    + chuyển trang thêm sách thành modal thêm sách.
    + Hoàn thiện lịch sử thao tác với sách.
    + Gợi ý bảng chọn ngày trong ô chọn ngày mượn/trả sách.
    + Hoàn thành lịch sử mượn sách
    + thay trang trả sách thành modal trả sách nhanh.
    + Hiển thị những lịch sử sách quá hạn.
    + Tạo lịch sử thêm xóa sửa thành viên.
