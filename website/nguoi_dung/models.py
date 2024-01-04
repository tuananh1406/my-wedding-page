# coding: utf-8
"""Model người dùng"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class NguoiDung(AbstractUser):
    """Model người dùng, các thông tin hiện tại bao gồm:
    - Họ và tên: ho_va_ten
    - Ngày sinh: ngay_sinh
    - Giới tính: gioi_tinh
    - Địa chỉ: dia_chi
    - Điện thoại: dien_thoai
    """

    ho_va_ten = models.CharField(
        "Họ và tên",
        max_length=200,
        null=True,
    )
    ngay_sinh = models.DateField(
        "Ngày sinh",
        null=True,
    )
    gioi_tinh = models.CharField(
        "Giới tính",
        max_length=30,
        null=True,
    )
    dia_chi = models.CharField(
        "Địa chỉ",
        max_length=200,
        null=True,
    )
    dien_thoai = models.CharField(
        "Số điện thoại",
        max_length=20,
        null=True,
    )
    ma_xac_thuc = models.UUIDField(
        "Mã xác thực",
        default=uuid.uuid4,
    )

    class Meta:
        """Khai báo các thuộc tính của model, gồm:
        - Trường sắp xếp thứ tự: username
        - Tên hiển thị: Người dùng
        - Tên hiển thị đầy đủ: Danh sách Người dùng
        """

        ordering = ["username"]
        verbose_name = "Người dùng"
        verbose_name_plural = "Danh sách Người dùng"
