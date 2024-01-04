import random

from django.views.generic import TemplateView

# Create your views here.


class ILoveYou(TemplateView):
    """Theme tỏ tình crush"""

    template_name = "i-love-you/index.html"


class NewYear(TemplateView):
    """Theme chúc mừng năm mới"""

    template_name = "new-year/index.html"


class Cube3D(TemplateView):
    """Theme Cube 3D"""

    template_name = "cube/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ds_anh = random.sample(range(1, 15), 6)
        context["ds_anh_100"] = [f"anh_ca_nhan/100/{stt}_100.jpg" for stt in ds_anh]
        context["ds_anh_100"][1] += "-rotate"
        context["ds_anh_400"] = [f"anh_ca_nhan/400/{stt}_400.jpg" for stt in ds_anh]
        context["ds_anh_400"][1] += "-rotate"
        context["tieu_de"] = "❤❤❤ Hữu Tuấn Anh ❤❤❤"
        context["audio"] = "cube/audio/1.mp3"
        context["anh_nen"] = f"cube/js/{random.randrange(1, 5)}.js"

        return context


class ScrollbarGallery(TemplateView):
    """https://codepen.io/TheMOZZARELLA/pen/oNpMxyy"""

    template_name = "photo_gallery_themes/scrollbar_pagination.html"
