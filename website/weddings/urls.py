from django.urls import path
from django.views.decorators.cache import cache_page
from weddings.views import (
    ViewGlanzGolden,
    ViewGuiLoiChuc,
    ViewMyWedding,
    ViewTatCaLoiChuc,
    ViewTrueLove,
    ViewTrueLoveComingSoon,
    ViewTrueLoveCustom,
    ViewTrueLoveInvitation,
    ViewCountDays,
)

app_name = "weddings"

urlpatterns = [
    path("my-wedding/", ViewMyWedding.as_view(), name="my_wedding"),
    path("true-love/", ViewTrueLove.as_view(), name="true_love"),
    path(
        "true-love/<slug:slug>", ViewTrueLoveCustom.as_view(), name="true_love_custom"
    ),
    path(
        "true-love/invitation/<uuid:uid>",
        ViewTrueLoveInvitation.as_view(),
        name="true_love_invitation",
    ),
    path(
        "true-love/coming-soon/", ViewTrueLoveComingSoon.as_view(), name="coming_soon"
    ),
    path("glanz/golden", ViewGlanzGolden.as_view(), name="true_love"),
    path("love-story/", ViewCountDays.as_view(), name="love_story"),
    path("gui_loi_chuc/", ViewGuiLoiChuc.as_view(), name="gui_loi_chuc"),
    path(
        "true-love/nhung-loi-chuc/<int:pk_id>",
        cache_page(60 * 5)(ViewTatCaLoiChuc.as_view()),
        name="nhung_loi_chuc",
    ),
]
