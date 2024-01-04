from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.middleware.csrf import get_token
from django.views import View
from django.views.generic import TemplateView
from weddings.forms import FormWish
from weddings.models import (
    ImportantDay,
    LoveStory,
    Person,
    Photo,
    Wedding,
    Wish,
    Invitation,
)
from datetime import datetime


# Create your views here.
class ViewMyWedding(TemplateView):
    """Giao diện My wedding
    http://kamleshyadav.com/html/wedding/?storefront=envato-elements
    """

    template_name = "my_wedding/my_wedding.html"


class ViewTrueLove(TemplateView):
    """Giao diện True love
    https://html.themexriver.com/true-love/?storefront=envato-elements#main
    """

    template_name = "true_love/true_love.html"


class ViewTrueLoveCustom(TemplateView):
    """Giao diện True love
    https://html.themexriver.com/true-love/?storefront=envato-elements#main
    """

    template_name = "true_love/true_love_custom.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if slug := kwargs.get("slug"):
            if wedding := list(
                Wedding.objects.select_related(
                    "chu_re__donate_box", "co_dau__donate_box"
                ).filter(slug=slug)
            ):
                self._lay_thong_tin_wedding(wedding, context)
        return context

    def _lay_thong_tin_wedding(self, wedding, context):
        wedding_info = wedding[0]
        og_url = self.request.build_absolute_uri(
            reverse("weddings:true_love_custom", kwargs={"slug": wedding_info.slug})
        )
        og_image_url = self.request.build_absolute_uri(wedding_info.preview_image.url)
        love_stories = LoveStory.objects.filter(wedding=wedding_info).order_by(
            "ngay_ky_niem"
        )
        events = ImportantDay.objects.filter(wedding=wedding_info).order_by(
            "ngay_dien_ra"
        )
        photos = (
            Photo.objects.filter(wedding=wedding_info)
            .prefetch_related("phan_loai")
            .order_by("id")
        )
        families = Person.objects.filter(
            relationship__code="BM",
            nguoi_lien_quan__in=[wedding_info.chu_re, wedding_info.co_dau],
        )

        context["wedding_info"] = wedding_info
        context["og_url"] = og_url
        context["og_image_url"] = og_image_url
        context["love_stories"] = list(love_stories)
        context["events"] = list(events)
        context["slide_photos"] = []
        context["gallery"] = []
        context["wish_form"] = FormWish()
        context["wish_form"].fields["wedding"].widget.attrs.update(
            {
                "value": wedding_info.id,
            }
        )
        # context["wishes"] = wishes

        for photo in photos:
            if photo.is_slide:
                context["slide_photos"].append(photo)
            else:
                context["gallery"].append(photo)

        context["photo_filter"] = {
            (phan_loai.code, phan_loai.ten)
            for photo in photos
            for phan_loai in photo.phan_loai.all()
            if photo.phan_loai.all()
        }
        if families:
            context["families"] = {
                "ong_noi": families.get(
                    nguoi_lien_quan=wedding_info.chu_re, gioi_tinh="NAM"
                ),
                "ba_noi": families.get(
                    nguoi_lien_quan=wedding_info.chu_re, gioi_tinh="NU"
                ),
                "ong_ngoai": families.get(
                    nguoi_lien_quan=wedding_info.co_dau, gioi_tinh="NAM"
                ),
                "ba_ngoai": families.get(
                    nguoi_lien_quan=wedding_info.co_dau, gioi_tinh="NU"
                ),
            }


class ViewTrueLoveComingSoon(TemplateView):
    """Giao diện True love - Coming soon
    https://html.themexriver.com/true-love/?storefront=envato-elements#main
    """

    template_name = "true_love/coming-soon.html"


class ViewGlanzGolden(TemplateView):
    """Giao diện Glanz Golden
    http://glanz.starkethemes.com/html/01_03_home_golden.html
    """

    template_name = "glanz/golden/golden.html"


class ViewGuiLoiChuc(View):
    """Lưu lời chúc gửi qua form"""

    def post(self, request):
        """Nhận lời chúc gửi từ trang web"""

        form_data = FormWish(self.request.POST)
        data = {
            "is_valid": False,
        }
        if form_data.is_valid():
            form_data.save()
            data = {
                "is_valid": True,
            }
        return JsonResponse(data)

    def get(self, request):
        """Lấy csrf token"""
        token = get_token(request)
        return JsonResponse({"token": token})


class ViewTatCaLoiChuc(TemplateView):
    """Những lời chúc đã gửi"""

    template_name = "true_love/loi_chuc_da_gui.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if pk := kwargs.get("pk_id"):
            if wedding := Wedding.objects.select_related("chu_re", "co_dau").filter(
                id=pk
            ):
                wishes = Wish.objects.filter(wedding=wedding[0]).order_by("-created_at")
                context["wishes"] = wishes
        return context


class ViewTrueLoveInvitation(TemplateView):
    """Giao diện thiệp mời True love"""

    template_name = "true_love/true_love_invitation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if uid := kwargs.get("uid"):
            if invitation := list(
                Invitation.objects.prefetch_related(
                    "nguoi_lien_quan__chu_re",
                    "nguoi_lien_quan__co_dau",
                ).filter(uid=uid)
            ):
                weddings = (
                    invitation[0].nguoi_lien_quan.chu_re.all()
                    or invitation[0].nguoi_lien_quan.co_dau.all()
                )
                ngay_to_chuc = weddings[0].ngay_to_chuc
                invitation_data = invitation[0]
                friend_pronoun, my_pronoun = invitation_data.cach_xung_ho.split("/")
                og_img_ratio = invitation_data.width_anh_goc / 256
                og_img_height = int(invitation_data.height_anh_goc / og_img_ratio)
                context["invitation_info"] = {
                    "ngay_to_chuc": ngay_to_chuc
                    if invitation_data.nguoi_lien_quan.gioi_tinh == "NAM"
                    else datetime.strptime("14-11-2023", "%d-%m-%Y").date(),
                    "ten": invitation_data.ten,
                    "facebook_id": invitation_data.facebook_id,
                    "resid": invitation_data.resid,
                    "authkey": invitation_data.authkey,
                    "width_anh_goc": invitation_data.width_anh_goc,
                    "og_img_width": 256,
                    "og_img_height": og_img_height,
                    "friend_pronoun": friend_pronoun,
                    "my_pronoun": my_pronoun,
                }
        return context

    def get(self, request, *args, **kwargs):
        template = super().get(self, request, *args, **kwargs)
        if "invitation_info" in template.context_data.keys():
            return template
        else:
            return HttpResponseRedirect(
                reverse(
                    "weddings:true_love_custom", kwargs={"slug": "tuan-anh-kim-oanh"}
                )
            )


class ViewCountDays(TemplateView):
    """Đếm ngày yêu nhau"""

    template_name = "love_story/count_days.html"
