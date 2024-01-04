# -*- coding: utf-8 -*-
import io
from urllib.request import urlopen

import cv2
import numpy as np
import segno
from PIL import Image

from django.core.files.base import ContentFile
from zipfile import ZipFile


def read_image_from_url(url):
    with urlopen(url) as resp:
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image


def read_image_from_django_file(file_object):
    with file_object.open("rb") as file_content:
        image = np.asarray(bytearray(file_content.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image


def read_qrcode_from_image(image):
    detector = cv2.QRCodeDetector()
    value, _, _ = detector.detectAndDecode(image)
    return value


def get_file_name_and_ext_of_file_field(file_object):
    full_file_name = file_object.name.split("/")[-1]
    file_ext = full_file_name.split(".")[-1]
    file_name = full_file_name[: -(len(file_ext) + 1)]
    return file_name, file_ext


def create_new_qr_code(
    new_qr_code_field, background_photo_field, qr_data, new_qr_code_file_name
):
    with io.BytesIO() as out:
        with background_photo_field.open("rb") as bg_image:
            qr_code = segno.make(qr_data, error="h", mask=7)
            out = io.BytesIO()
            qr_code.to_artistic(background=bg_image, target=out, scale=10, kind="webp")

        new_qr_code_field.save(
            f"{new_qr_code_file_name}.webp", ContentFile(out.getvalue()), save=False
        )
    return True


def create_new_qr_code_with_logo(
    new_qr_code_field,
    logo_photo_field,
    new_qr_code_with_logo_field,
    new_qr_code_with_logo_file_name,
):
    with io.BytesIO() as out:
        with new_qr_code_field.open("rb") as qr_image:
            if logo_photo_field:
                with logo_photo_field.open("rb") as logo_image:
                    add_logo_to_qr_code(qr_image, logo_image, out)
            else:
                add_logo_to_qr_code(qr_image, None, out)
        new_qr_code_with_logo_field.save(
            f"{new_qr_code_with_logo_file_name}_with_logo.webp",
            ContentFile(out.getvalue()),
            save=False,
        )


def add_logo_to_qr_code(qr_image, logo_image, out):
    qr_image.seek(0)

    img = Image.open(qr_image)
    img = img.convert("RGB")
    img_width, img_height = img.size
    logo_max_size = img_height // 4

    if logo_image is not None:
        logo_image.seek(0)
        logo_img = Image.open(logo_image)
        logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
        box = (
            (img_width - logo_img.size[0]) // 2,
            (img_height - logo_img.size[1]) // 2,
        )
        img.paste(logo_img, box)
    img.save(out, format="webp")


def extract_zip_file(zip_file_field, photo_class, name, phan_loai, wedding, gioi_thieu):
    zip_obj = ZipFile(zip_file_field, mode="r")
    # return {name: zip_obj.read(name) for name in zip_obj.namelist()}
    list_file_paths = [
        file_path
        for file_path in zip_obj.namelist()
        if "macosx" not in file_path.lower() and len(file_path.split(".")) == 2
    ]
    for file_path in list_file_paths:
        with io.BytesIO() as out:
            out.write(zip_obj.read(file_path))
            out.seek(0)
            full_file_name = file_path.split("/")[-1]
            new_photo = photo_class()
            new_photo.ten = name
            new_photo.gioi_thieu = gioi_thieu
            new_photo.wedding = wedding
            new_photo.hinh_anh.save(file_path, ContentFile(out.getvalue()), save=True)
            new_photo.phan_loai.add(*phan_loai)
    return list_file_paths


def tao_slug(ket_qua):
    """Hàm tạo chuỗi tiếng việt không dấu"""
    mautimkiem = {
        "[àáảãạăắằẵặẳâầấậẫẩ]": "a",
        "[đ]": "d",
        "[èéẻẽẹêềếểễệ]": "e",
        "[ìíỉĩị]": "i",
        "[òóỏõọôồốổỗộơờớởỡợ]": "o",
        "[ùúủũụưừứửữự]": "u",
        "[ỳýỷỹỵ]": "y",
        " ": "-",
    }
    ket_qua = re.sub(r"^\s+", "", ket_qua)
    ket_qua = re.sub(r"\s+$", "", ket_qua)
    for mau, thaythe in mautimkiem.items():
        ket_qua = re.sub(mau, thaythe, ket_qua)
        ket_qua = re.sub(mau.upper(), thaythe.upper(), ket_qua)
    return ket_qua.lower()


def kiem_tra_slug(slug, list_exists_slugs):
    """Hàm tạo slug không bị trùng"""
    is_duplicate = False
    list_exists_numbers = []
    for exists_slug in list(list_exists_slugs):
        if isinstance(exists_slug, (list, tuple)):
            exists_slug = exists_slug[0] if exists_slug else ""
        if re.match(f"^{slug}-*\d*$", exists_slug):
            is_duplicate = True
            last_number = exists_slug.split("-")[-1]
            if last_number.isdigit():
                list_exists_numbers.append(int(last_number))

    if is_duplicate:
        max_number = max(list_exists_numbers, default=0)
        return f"{slug}-{max_number + 1}"
    return slug


def luu_anh_theo_ten(model, tep_tai_len):
    """Hàm tạo đường dẫn ảnh theo tên"""
    dinh_dang = tep_tai_len.split(".")[-1]
    ten_tep = False
    for ten_thuoc_tinh in [
        "ten",
        "tieu_de",
        "ho_va_ten",
        "slug",
    ]:
        if hasattr(model, ten_thuoc_tinh):
            ten_tep = str(tao_slug(getattr(model, ten_thuoc_tinh)))
    if ten_tep:
        ten_tep_moi = ".".join([ten_tep, dinh_dang])
        ten_thu_muc = str(tao_slug(model._meta.verbose_name))
        STT = 0
        while True:
            if ten_thu_muc is not None:
                duong_dan = os.path.join(ten_thu_muc, ten_tep_moi)
            else:
                duong_dan = ten_tep_moi
            if os.path.exists(duong_dan):
                STT += 1
                ten_tep_moi = "-".join([ten_tep_moi, STT])
                continue
            break
        return duong_dan
