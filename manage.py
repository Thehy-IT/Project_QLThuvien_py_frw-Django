"""Django's command-line utility for administrative tasks."""
import os # quản lý biên smooi trường
import sys # quản lý hệ thống, cho phép truy cập vào các đối tượng và hàm của hệ thống


def main():
    """Run administrative tasks."""
    # Thiết lập biến môi trường để Django biết nơi tìm kiếm cài đặt
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
    try:# thử import Django và kiểm tra thông báo.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
