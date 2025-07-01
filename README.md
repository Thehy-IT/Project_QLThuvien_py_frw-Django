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

## Ảnh giới thiệu hệ thống
trang chủ:
![Trang chủ](/src/static/images/trangchu.png)
quản lý sách:
![Quản lý sách](/src/static/images/quanlysach.png)
lọc sách:
![Lọc sách](/src/static/images/locsach.png)
quản lý thành viên:
![Quản lý thành viên](/src/static/images/thanhvinen.png)
thêm thành viên:
![Thêm thành viên](/src/static/images/themthanhvien.png)
mượn sách:
![Mượn sách](/src/static/images/muonsach.png)
trả sách nhanh:
![Trả sách nhanh](/src/static/images/trasach.png)
mượn quá hạn:
![Mượn quá hạn](/src/static/images/muonquahan.png)


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
    - tạo giao diện đăng nhập/đăng ký.
    - trực quan hóa biểu đồ thống kê sách, thành viên riêng.
    - Hoàn thiện tất cả các thẻ lịch sử.
    + tạo id tự động cho mỗi phần mẫu đăng ký mượn sách.
    + tạo id tự động cho mỗi form cần ID với số ID là só tiếp theo số đã có.
    + Cập nhật trạng thái sách trong quản lý sách khi nhấn trả sách thành công.
    + Phân trang cho danh sách sách, thành viên, lịch sử mượn sách.
