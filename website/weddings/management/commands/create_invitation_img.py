from django.core.management.base import BaseCommand
from weddings.models import Person, Invitation
import os
from uuid import uuid4
from django.conf import settings
from weddings.auto_web_utils import (
    chay_trinh_duyet,
    tam_ngung_va_tim,
    dang_nhap_facebook,
    luu_cookies,
    dang_nhap_bang_cookies,
    send_invitation,
    send_message,
    create_invitation_img,
    get_web_link_from_share_link,
    extract_share_link,
)


class Command(BaseCommand):
    help = "Tạo ảnh thiệp mới và lấy link chia sẻ"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("[+]Starting..."))
        invitation_path = "weddings/static/invitation"
        groom = Person.objects.get(id=1)
        bride = Person.objects.get(id=2)
        groom_invitation = os.path.join(invitation_path, "groom_invitation.png")
        groom_coor = (2170, 325)
        bride_invitation = os.path.join(invitation_path, "bride_invitation_upscale.png")
        font_path = os.path.join(invitation_path, "SVN-Graphitel.otf")
        bride_coor = (2030, 285)
        font_size = 110
        groom_default_img_info = {"width": 3624, "height": 2426}
        bride_default_img_info = {"width": 3356, "height": 2236}
        groom_persons = [
            # (
            #     "chị/em",
            #     "Ánh",
            #     "https://www.facebook.com/ngocanhk49",
            # ),
            # (
            #     "chị/em",
            #     "Thương",
            #     "https://www.facebook.com/bangthuong.nguyenthi",
            # ),
            # (
            #     "em/anh",
            #     "Yến",
            #     "https://www.facebook.com/profile.php?id=100006727185549",
            # ),
            # (
            #     "em/anh",
            #     "Ngọc",
            #     "https://www.facebook.com/tho.ngoc28",
            # ),
            # (
            #     "em/anh",
            #     "Phong",
            #     "https://www.facebook.com/profile.php?id=100005642198341",
            # ),
            # ("em/anh", "Sơn", "https://www.facebook.com/Ignatius2211"),
            # (
            #     "em/anh",
            #     "Trung",
            #     "https://www.facebook.com/profile.php?id=100034434909665",
            # ),
            # ("chị/em", "Hồng", "https://www.facebook.com/nhat.hong.3386"),
            # ("chị/em", "Hạnh", "https://www.facebook.com/chicky.bong"),
            # ("anh/em", "Mùi + gđ", ""),
            # (
            #     "anh/em",
            #     "Đức",
            #     "https://www.facebook.com/zkazus2",
            # ),
            # (
            #     "chị/em",
            #     "Vân Anh",
            #     "https://www.facebook.com/vananh.aries",
            # ),
            # ("bạn/mình", "Sơn", "https://www.facebook.com/jackdang.aries"),
            # # A5k88
            # ("bạn/mình", "Hồng", "https://www.facebook.com/tranthanhxhong"),
            # ("bạn/mình", "Tài", "https://www.facebook.com/us.sikai"),
            # ("bạn/mình", "Hưng", "https://www.facebook.com/hungphan2012"),
            # ("bạn/mình", "Lâm", "https://www.facebook.com/nguyenlam12193"),
            # ("bạn/mình", "Oanh", "https://www.facebook.com/blackchic14"),
            # (
            #     "bạn/mình",
            #     "Sơn",
            #     "https://www.facebook.com/profile.php?id=100013463970214",
            # ),
            # ("bạn/mình", "Tín", "https://www.facebook.com/tin.trung.7311"),
            # ("bạn/mình", "Nguyên + nt", ""),
            # ("bạn/mình", "Quân + nt", ""),
            # ("bạn/mình", "Hoàng + nt", ""),
            # ("bạn/mình", "Hùng + nt", ""),
            # ("bạn/mình", "Quang + nt", ""),
            # ("bạn/mình", "Thế + nt", ""),
            # ("bạn/mình", "Long + nt", ""),
            # ("bạn/mình", "Cường + nt", ""),
            # ("bạn/mình", "Huy + nt", ""),
            # # Bạn đại học
            ("bạn/mình", "Mạnh", ""),
            # ("bạn/mình", "Thảo", "https://www.facebook.com/trong.veo.180"),
            # ("em/anh", "Ly",
            # "https://www.facebook.com/profile.php?id=100008496362102"),
            # ("em/anh", "Dung", "https://www.facebook.com/tjeuvj.kjm"),
            # ("bạn/mình", "Hoàng", "https://www.facebook.com/salem.meo.35"),
            # ("bạn/mình", "Ngọc", "https://www.facebook.com/nguyentienngoc93"),
            # ("em/anh", "Phong", "https://www.facebook.com/phong.hyk"),
            # # Thầy cô dại học
            # ("cô/em", "Thành Vinh", "https://www.facebook.com/vinh.luongthithanh"),
            # ("chị/em", "Hà", "https://www.facebook.com/thuyha1991"),
            # ("cô/em", "Tuyến", "https://www.facebook.com/tuyenhung.khanhlinh"),
            # (
            #     "cô/em",
            #     "Trang Thanh",
            #     "https://www.facebook.com/trangthanh.nguyenthi.50",
            # ),
            # ("chị/em", "Linh", ""),
            # ("bạn/mình", "Lý", ""),
            # ("bạn/mình", "Việt Anh", ""),
            # ("bạn/mình", "Kim Anh", ""),
            # ("bạn/mình", "Tuấn Anh", ""),
            # ("bạn/mình", "Cảnh Đức", ""),
            # ("bạn/mình", "Bá Đức", ""),
            # ("bạn/mình", "Khuyên", ""),
            # ("bạn/mình", "Hạnh", ""),
            # VCCorp
            # ("em/anh", "Thái", "https://www.facebook.com/Petblack1998"),
            # ("em/anh", "Huy", "https://www.facebook.com/huyduong2792000"),
            # (
            #     "em/anh",
            #     "Tùng",
            #     "https://www.facebook.com/profile.php?id=100010097592791",
            # ),
            # ("em/anh", "Quang", "https://www.facebook.com/nquang782"),
            # Nhất nam
            # (
            #     "bạn/mình",
            #     "Đạo",
            #     "https://www.facebook.com/profile.php?id=100004647607332",
            # ),
            # ("bạn/mình", "Chương", "https://www.facebook.com/Vu.Chuong2605"),
            # ("anh/em", "Công", "https://www.facebook.com/hoangcongdz"),
            # ("bạn/mình", "My", "https://www.facebook.com/fkhjskd.tran"),
            # ("bạn/mình", "Thảo", "https://www.facebook.com/binh.thao.3"),
            # ("bạn/mình", "Thảo", "https://www.facebook.com/vi.thao.5076"),
            # Vinmec
            # (
            #     "anh/em",
            #     "Bình",
            #     "https://www.facebook.com/binh.nguyen.1090",
            # ),
            # Zen8
            # (
            #     "anh/em",
            #     "Nhật Anh",
            #     "https://www.facebook.com/anh.ngo.3363",
            # ),
            # ("anh/em", "Sơn", ""),
            # Leeon
            # ("Toàn thể/em", "Công ty Leeon Tech", ""),
            # ("anh/em", "Bình + gđ", ""),
            # ("anh/em", "Phúc + gđ", ""),
            # ("em/anh", "Nhi + nt", ""),
            # ("em/anh", "Trân + nt", ""),
            # ("em/anh", "Lâm", ""),
        ]
        bride_persons = [
            # ("bạn/mình", "Ngân + nt", ""),
            # ("bạn/mình", "Thu + nt", ""),
            # ("bạn/mình", "Thúy + nt", ""),
            # ("bạn/mình", "Tươi + gđ", ""),
            # ("bạn/mình", "Thắm + nt", ""),
            # ("bạn/mình", "Phương + gđ", ""),
            # ("anh/em", "Tuấn + gđ", ""),
            # ("anh/em", "An + gđ", ""),
            # ("chị/em", "Oanh + gđ", ""),
            # ("em/chị", "Sơn + nt", ""),
            # ("em/chị", "Thanh + nt", ""),
            # ("em/chị", "Cường + gđ", ""),
            # ("em/chị", "Duyên + nt", ""),
            # ("em/chị", "Trang + nt", ""),
            # ("em/chị", "Đạt + nt", ""),
            # ("em/chị", "Tùng + nt", ""),
            # ("em/chị", "Ngọc + nt", ""),
            # ("em/chị", "Hùng + nt", ""),
            # ("bạn/mình", "Quỳnh + nt", ""),
            # ("em/chị", "Độ + nt", ""),
        ]

        create_for = "groom"
        if create_for == "groom":
            nguoi_lien_quan = groom
            invitation_template = groom_invitation
            coor = groom_coor
            persons = groom_persons
            default_image_infor = groom_default_img_info
        else:
            nguoi_lien_quan = bride
            invitation_template = bride_invitation
            coor = bride_coor
            persons = bride_persons
            default_image_infor = bride_default_img_info

        # Gửi tin nhắn facebook mời bạn bè
        self.stdout.write(self.style.SUCCESS(f"[+]Tạo thiệp cho: {create_for}"))
        for pronoun, friend_name, friend_facebook_link in persons:
            friend_pronoun, my_pronoun = pronoun.split("/")
            if friend_facebook_link:
                if "id=" in friend_facebook_link:
                    friend_id = friend_facebook_link.split("=")[-1]
                else:
                    friend_id = friend_facebook_link.strip("/").rsplit("/", maxsplit=1)[
                        -1
                    ]
            else:
                friend_id = None

            self.stdout.write(self.style.SUCCESS("Tạo ảnh thiệp mời"))
            new_uid = uuid4()
            share_link = create_invitation_img(
                invitation_path,
                invitation_template,
                coor,
                font_path,
                font_size,
                friend_pronoun,
                friend_name,
                friend_id,
                new_uid,
            )
            self.stdout.write(self.style.SUCCESS("Lấy web_link"))
            web_link, image_info = get_web_link_from_share_link(share_link)
            if not image_info:
                image_info = default_image_infor
            self.stdout.write(
                self.style.SUCCESS(f"{friend_pronoun} {friend_name}: {web_link}")
            )
            self.stdout.write(
                self.style.SUCCESS(f"{friend_pronoun} {friend_name}: {image_info}")
            )
            res_id, auth_key = extract_share_link(web_link)
            photo_share_link = (
                f"https://onedrive.live.com/embed?resid={res_id}&au"
                f"thkey={auth_key}&width={image_info.get('width')}"
            )
            self.stdout.write(self.style.SUCCESS(f"{photo_share_link}"))
            new_invitation = Invitation()
            new_invitation.uid = new_uid
            new_invitation.nguoi_lien_quan = nguoi_lien_quan
            new_invitation.ten = friend_name
            new_invitation.facebook_id = friend_id
            new_invitation.cach_xung_ho = pronoun
            new_invitation.width_anh_goc = image_info.get("width")
            new_invitation.height_anh_goc = image_info.get("width")
            new_invitation.resid = res_id
            new_invitation.authkey = auth_key
            new_invitation.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"https://huutuananh.com/weddings/true-love/invitation/{new_invitation.uid}"
                )
            )
