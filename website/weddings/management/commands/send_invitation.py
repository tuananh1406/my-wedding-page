from django.core.management.base import BaseCommand
from weddings.models import Person, Invitation
import os
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
)
from django.urls import reverse


class Command(BaseCommand):
    help = "Tạo ảnh thiệp mới và lấy link chia sẻ"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("[+]Starting..."))
        invitation_path = "weddings/static/invitation"
        groom = Person.objects.get(id=1)
        bride = Person.objects.get(id=2)
        groom_cookies = os.path.join(invitation_path, "groom_main_cookies.bak")
        bride_cookies = os.path.join(invitation_path, "bride_cookies.bak")
        groom_wedding_day = "18/11/2023"
        groom_persons = Invitation.objects.filter(
            nguoi_lien_quan=groom, facebook_id__isnull=False, is_sended=False
        )

        # Gửi tin nhắn facebook mời bạn bè
        self.stdout.write(self.style.SUCCESS("[+]Groom:"))
        self.stdout.write(self.style.SUCCESS("[+]Mở Facebook:"))
        driver = None
        try:
            driver = chay_trinh_duyet(headless=False)
            if os.path.exists(groom_cookies):
                self.stdout.write(self.style.SUCCESS("Đăng nhập bằng cookies"))
                driver = dang_nhap_bang_cookies(driver, groom_cookies)
            else:
                self.stdout.write(self.style.SUCCESS("[+]Đăng nhập Facebook:"))
                driver = dang_nhap_facebook(driver)
                self.stdout.write(self.style.SUCCESS("Lưu cookies"))
                groom_cookies_saved = luu_cookies(driver, groom_cookies)
                self.stdout.write(
                    self.style.SUCCESS(f"Cookies được lưu vào: {groom_cookies}")
                )

            for person in groom_persons:
                friend_pronoun, my_pronoun = person.cach_xung_ho.split("/")
                invitation_uri = reverse(
                    "weddings:true_love_invitation", kwargs={"uid": person.uid}
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Gửi thiệp mời cho {person.facebook_id}")
                )
                send_invitation(
                    driver,
                    groom_wedding_day,
                    my_pronoun,
                    friend_pronoun,
                    person.ten,
                    person.facebook_id,
                    f"https://huutuananh.com{invitation_uri}",
                )
                person.is_sended = True
                person.save()
            input()
        except Exception as error:
            print(error)
        finally:
            if driver:
                driver.close()
