from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import TaoNguoiDung, ThayDoiNguoiDung

# Register your models here.
NguoiDung = get_user_model()


class NguoiDungAdmin(UserAdmin):
    add_form = TaoNguoiDung
    form = ThayDoiNguoiDung
    model = NguoiDung
    list_display = [
        "email",
        "username",
    ]


admin.site.register(NguoiDung, NguoiDungAdmin)
