from django.urls import path

from custom import views

app_name = "custom"

urlpatterns = [
    path("i-love-you/", views.ILoveYou.as_view(), name="i_love_you"),
    path("love/", views.Cube3D.as_view(), name="love"),
    path("happy-new-year/", views.NewYear.as_view(), name="happy-new-year"),
    path("scrollbar/", views.ScrollbarGallery.as_view(), name="scrollbar_pagination"),
]
