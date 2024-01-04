from django.contrib.auth import get_user_model
from django.test import TestCase


# Create your tests here.
class KiemTraNguoiDung(TestCase):
    def setUp(self):
        # Khởi tạo các giá trị mặc định

        # Người dùng
        self.ten_dang_nhap = "test1"
        self.email = "test1@mail.com"
        self.mat_khau = "kiemtra123"

        # Quản trị viên
        self.ten_dang_nhap_qtv = "quan_tri1"
        self.email_qtv = "quan_tri1@mail.com"

    def test_tao_nguoi_dung(self):
        # Kiểm tra hàm tạo người dùng
        NguoiDung = get_user_model()
        nguoi_dung = NguoiDung.objects.create_user(
            username=self.ten_dang_nhap,
            email=self.email,
            password=self.mat_khau,
        )
        self.assertEqual(nguoi_dung.username, self.ten_dang_nhap)
        self.assertEqual(nguoi_dung.email, self.email)
        self.assertTrue(nguoi_dung.is_active)
        self.assertFalse(nguoi_dung.is_staff)
        self.assertFalse(nguoi_dung.is_superuser)

    def test_tao_quan_tri_vien(self):
        # Kiểm tra tạo tài khoản quản trị viên
        NguoiDung = get_user_model()
        quan_tri_vien = NguoiDung.objects.create_superuser(
            username=self.ten_dang_nhap_qtv,
            email=self.email_qtv,
            password=self.mat_khau,
        )
        self.assertEqual(quan_tri_vien.username, self.ten_dang_nhap_qtv)
        self.assertEqual(quan_tri_vien.email, self.email_qtv)
        self.assertTrue(quan_tri_vien.is_active)
        self.assertTrue(quan_tri_vien.is_staff)
        self.assertTrue(quan_tri_vien.is_superuser)
