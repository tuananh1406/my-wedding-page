from uuid import uuid4
from django.db import models
from weddings.utils import (
    create_new_qr_code,
    kiem_tra_slug,
    luu_anh_theo_ten,
    tao_slug,
    create_new_qr_code_with_logo,
    get_file_name_and_ext_of_file_field,
    read_image_from_django_file,
    read_image_from_url,
    read_qrcode_from_image,
    extract_zip_file,
)

# Create your models here.
GIOI_TINH = [
    ("NAM", "Nam"),
    ("NU", "Nữ"),
]


class PersonGroup(models.Model):
    # Chia nhóm người tham gia
    ten_nhom = models.CharField(
        "Tên nhóm",
        max_length=255,
    )

    class Meta:
        ordering = ["ten_nhom"]
        verbose_name_plural = "Nhóm người tham gia"

    def __str__(self):
        return str(self.ten_nhom)


class Relationship(models.Model):
    ten = models.CharField(
        "Tên mối quan hệ",
        max_length=255,
    )
    code = models.CharField("Mã mối quan hệ", max_length=10, null=True, blank=True)
    chi_tiet = models.CharField(
        "Chi tiết mối quan hệ", max_length=255, null=True, blank=True
    )

    class Meta:
        ordering = ["ten"]
        verbose_name_plural = "Mối quan hệ"

    def __str__(self):
        return str(self.ten)


class DonateBox(models.Model):
    "Hộp mừng cưới"
    ten = models.CharField(
        "Tiêu đề hình ảnh",
        max_length=255,
    )
    qr_code_image = models.ImageField(
        "Mã QR", upload_to="qr_codes/", null=True, blank=True
    )
    qr_code_url = models.CharField(
        "URL qr code", null=True, blank=True, max_length=1000
    )
    background_photo = models.ImageField(
        "Ảnh nền cho QR mới", upload_to="qr_codes/", null=True, blank=True
    )
    logo_photo = models.ImageField(
        "Ảnh logo cho QR mới", upload_to="qr_codes/", null=True, blank=True
    )
    new_qr_code = models.ImageField(
        "Mã QR mới", upload_to="qr_codes/", null=True, blank=True
    )
    new_qr_code_with_logo = models.ImageField(
        "Mã QR mới có logo", upload_to="qr_codes/", null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Thông tin mừng cưới"

    def __str__(self):
        return f"{self.id} - {self.ten}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.qr_code_image:
            qr_image = read_image_from_django_file(self.qr_code_image)
            new_qr_code_file_name, _ = get_file_name_and_ext_of_file_field(
                self.qr_code_image
            )
        elif self.qr_code_url:
            qr_image = read_image_from_url(self.qr_code_url)
            new_qr_code_file_name = tao_slug(self.ten)
        else:
            qr_image = None
        if qr_image is not None and self.background_photo:
            qr_data = read_qrcode_from_image(qr_image)
            create_new_qr_code(
                self.new_qr_code, self.background_photo, qr_data, new_qr_code_file_name
            )
            create_new_qr_code_with_logo(
                self.new_qr_code,
                self.logo_photo,
                self.new_qr_code_with_logo,
                new_qr_code_file_name,
            )
            super().save(*args, **kwargs)


class Person(models.Model):
    # Người tham gia
    ho_va_ten = models.CharField(
        "Họ và tên",
        max_length=255,
    )
    ten_rut_gon = models.CharField("Tên rút gọn", max_length=255, null=True, blank=True)
    ten_viet_tat = models.CharField(
        "Tên viết tắt", max_length=255, null=True, blank=True
    )
    ten_thay_the = models.CharField(
        "Tên thay thế", max_length=255, blank=True, null=True
    )
    ngay_sinh = models.DateField(
        auto_now_add=False, verbose_name="Ngày sinh", blank=True, null=True
    )
    gioi_tinh = models.CharField(
        "Giới tính", max_length=3, choices=GIOI_TINH, default="NU"
    )
    gioi_thieu = models.CharField(
        "Giới thiệu về bản thân", max_length=1000, null=True, blank=True
    )
    facebook = models.CharField(
        "Link facebook cá nhân", max_length=255, blank=True, null=True
    )
    email = models.CharField("Email", max_length=255, blank=True, null=True)
    so_dien_thoai = models.CharField(
        "Số điện thoại", max_length=255, blank=True, null=True
    )
    ten_nhom = models.ForeignKey(
        PersonGroup,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Tên nhóm",
    )
    relationship = models.ForeignKey(
        Relationship,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Mối quan hệ",
    )
    nguoi_lien_quan = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Người liên quan",
    )
    loi_nhan_gui = models.CharField(
        "Lời nhắn gửi tới người tham gia", max_length=255, null=True, blank=True
    )
    hinh_anh = models.ImageField(
        "Hình ảnh", upload_to=luu_anh_theo_ten, null=True, blank=True
    )
    donate_box = models.ForeignKey(
        DonateBox,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donate_box",
        verbose_name="Mừng cưới",
    )
    kha_nang_tham_gia = models.BooleanField("Khả năng tham gia", default=False)
    url_invitation = models.CharField(
        "Đường dẫn hình ảnh thiệp mời", max_length=255, null=True, blank=True
    )
    donated_value = models.IntegerField("Số tiền mừng", default=0)

    class Meta:
        ordering = ["ho_va_ten"]
        verbose_name_plural = "Người tham gia"

    def __str__(self):
        return str(self.ho_va_ten)

    def save(self, *args, **kwargs):
        list_ho_ten = self.ho_va_ten.split(" ")
        if len(list_ho_ten) >= 2:
            self.ten_rut_gon = " ".join(list_ho_ten[-2:])
        else:
            self.ten_rut_gon = self.ho_va_ten
        super().save(*args, **kwargs)


class Wedding(models.Model):
    # New wedding
    chu_re = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        related_name="chu_re",
        limit_choices_to={"gioi_tinh": "NAM"},
        verbose_name="Chú rể",
    )
    hinh_nen = models.ImageField(
        "Hình nền", upload_to=luu_anh_theo_ten, null=True, blank=True
    )
    co_dau = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        related_name="co_dau",
        limit_choices_to={"gioi_tinh": "NU"},
        verbose_name="Cô dâu",
    )
    ngay_to_chuc = models.DateField(
        auto_now_add=False,
        verbose_name="Ngày tổ chức lễ cưới",
    )
    thong_bao = models.CharField(
        "Thông báo lễ cưới", max_length=1000, null=True, blank=True
    )
    logo = models.ImageField("Logo", upload_to=luu_anh_theo_ten, null=True, blank=True)
    logo_sm = models.ImageField(
        "Logo SM", upload_to=luu_anh_theo_ten, null=True, blank=True
    )
    preview_image = models.ImageField(
        "Hình xem trước khi chia sẻ (1200x630)",
        upload_to=luu_anh_theo_ten,
        null=True,
        blank=True,
    )
    preview_image_type = models.CharField(
        "Định dạng hình ảnh (image/jpeg)",
        max_length=30,
        null=True,
        blank=True,
        default="image/jpeg",
    )
    description_share = models.CharField(
        "Mô tả ngắn khi chia sẻ. 2 - 4 câu", max_length=1000, null=True, blank=True
    )
    hinh_nen_loi_chuc = models.ImageField(
        "Hình nền lời chúc", upload_to=luu_anh_theo_ten, null=True, blank=True
    )
    duong_dan_youtube = models.CharField(
        "Đường dẫn video youtube",
        max_length=1000,
        null=True,
        blank=True,
    )
    slug = models.CharField("Đường dẫn rút gọn", max_length=1000, null=True, blank=True)

    class Meta:
        ordering = ["ngay_to_chuc"]
        verbose_name_plural = "Lễ cưới"

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_chu_re = tao_slug(self.chu_re.ten_rut_gon)
            slug_co_dau = tao_slug(self.co_dau.ten_rut_gon)
            self.slug = f"{slug_chu_re}-{slug_co_dau}"
            list_exists_slugs = Wedding.objects.only("slug").all().values_list("slug")
            self.slug = kiem_tra_slug(self.slug, list_exists_slugs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.chu_re.ho_va_ten} - {self.co_dau.ho_va_ten}"


class ImportantDay(models.Model):
    "Ngày trọng đại"
    ten = models.CharField(
        "Tên ngày trọng đại",
        max_length=255,
    )
    ngay_dien_ra = models.DateField(
        auto_now_add=False,
        verbose_name="Ngày diễn ra sự kiện",
    )
    thoi_gian_bat_dau = models.TimeField(
        auto_now_add=False,
        verbose_name="Thời gian bắt đầu",
    )
    thoi_gian_ket_thuc = models.TimeField(
        auto_now_add=False,
        verbose_name="Thời gian kết thúc",
    )
    dia_diem = models.CharField(
        "Địa điểm tổ chúc",
        max_length=255,
    )
    map_url = models.CharField(
        "Đường dẫn google map", max_length=255, null=True, blank=True
    )
    hinh_anh = models.ImageField(
        "Hình ảnh", upload_to=luu_anh_theo_ten, null=True, blank=True
    )
    gioi_thieu = models.CharField(
        "Giới thiệu nội dung buổi lễ",
        max_length=1000,
        null=True,
        blank=True,
    )
    wedding = models.ForeignKey(
        Wedding,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Lễ cưới",
    )

    class Meta:
        ordering = ["ngay_dien_ra"]
        verbose_name_plural = "Ngày trọng đại"

    def __str__(self):
        return str(self.ten)


class LoveStory(models.Model):
    "Chuyện tình yêu"
    ten = models.CharField(
        "Tên mẩu chuyện",
        max_length=255,
    )
    ngay_ky_niem = models.DateField(
        auto_now_add=False,
        verbose_name="Ngày kỷ niệm",
    )
    noi_dung = models.CharField(
        "Nội dung mẩu chuyện",
        max_length=255,
    )
    wedding = models.ForeignKey(
        Wedding,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Lễ cưới",
    )
    hinh_anh = models.ImageField(
        "Hình ảnh", upload_to=luu_anh_theo_ten, null=True, blank=True
    )

    class Meta:
        ordering = ["ngay_ky_niem"]
        verbose_name_plural = "Chuyện tình yêu"

    def __str__(self):
        return str(self.ten)


class PhotoType(models.Model):
    "Phân loại hình ảnh"
    ten = models.CharField(
        "Tên phân loại",
        max_length=255,
    )
    code = models.CharField(
        "Mã phân loại",
        max_length=50,
    )

    class Meta:
        verbose_name_plural = "Phân loại hình ảnh"

    def __str__(self):
        return f"{self.code} - {self.ten}"


class Photo(models.Model):
    "Hình ảnh"
    ten = models.CharField(
        "Tiêu đề hình ảnh",
        max_length=255,
    )
    gioi_thieu = models.CharField(
        "Giới thiệu về hình ảnh", max_length=255, null=True, blank=True
    )
    hinh_anh = models.ImageField(
        "Hình ảnh", upload_to=luu_anh_theo_ten, null=True, blank=True
    )
    phan_loai = models.ManyToManyField(
        PhotoType,
        verbose_name="Phân loại ảnh",
        blank=True,
        related_name="phan_loai_anh",
    )
    is_slide = models.BooleanField("Ảnh trong slider", default=False)
    wedding = models.ForeignKey(
        Wedding,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Lễ cưới",
    )

    class Meta:
        verbose_name_plural = "Hình ảnh đám cưới"

    def __str__(self):
        return f"{self.id} - {self.ten}"


class Wish(models.Model):
    "Lời chúc"
    name = models.CharField(
        "Tên người gửi",
        max_length=255,
    )
    phone = models.CharField(
        "Số điện thoại",
        max_length=255,
    )
    email = models.CharField("Email", max_length=255, null=True, blank=True)
    facebook = models.CharField("Link facebook", max_length=255, null=True, blank=True)
    message = models.CharField(
        "Nội dung lời chúc",
        max_length=1000,
    )
    wedding = models.ForeignKey(
        Wedding,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Lễ cưới",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Lời chúc"

    def __str__(self):
        return f"{self.name} - {self.message}"


class PhotosZip(models.Model):
    "File ảnh nén"
    ten = models.CharField("Tên file", max_length=255, null=True, blank=True)
    zip_file = models.FileField(
        "File zip", upload_to="zip_files/", null=True, blank=True
    )
    is_extracted = models.BooleanField("Đã giải nén", default=False)
    phan_loai = models.ManyToManyField(
        PhotoType,
        verbose_name="Phân loại ảnh",
        blank=True,
        related_name="zip_phan_loai",
    )
    wedding = models.ForeignKey(
        Wedding,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Lễ cưới",
    )
    gioi_thieu = models.CharField(
        "Giới thiệu về hình ảnh", max_length=255, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.zip_file:
            list_file = extract_zip_file(
                self.zip_file,
                Photo,
                self.ten,
                self.phan_loai.all(),
                self.wedding,
                self.gioi_thieu,
            )

    class Meta:
        verbose_name_plural = "Ảnh nén"

    def __str__(self):
        return str(self.ten)


class Invitation(models.Model):
    "Thiệp mời"
    uid = models.UUIDField("uid", default=uuid4)
    nguoi_lien_quan = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="invitation_nguoi_lien_quan",
        verbose_name="Người liên quan",
    )
    ten = models.CharField(
        "Tên người nhận",
        max_length=255,
    )
    facebook_id = models.CharField("Facebook id", max_length=255, null=True, blank=True)
    cach_xung_ho = models.CharField(
        "Cách xưng hộ (cô/em)",
        max_length=255,
    )
    width_anh_goc = models.IntegerField("Width ảnh gốc")
    height_anh_goc = models.IntegerField("Height ảnh gốc", default=1)
    resid = models.CharField("resId", max_length=255)
    authkey = models.CharField("authkey", max_length=255)
    is_sended = models.BooleanField("Đã gửi", default=False)

    def __str__(self):
        return f"{self.ten}-{self.facebook_id}-{self.uid}"
