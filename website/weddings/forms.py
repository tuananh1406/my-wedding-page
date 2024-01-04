from django import forms
from weddings.models import Wish


class FormWish(forms.ModelForm):
    # Form liên hệ trong trang chủ
    class Meta:
        model = Wish
        fields = [
            "name",
            "phone",
            "email",
            "facebook",
            "message",
            "wedding",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "id": "name",
                    "class": "form-control",
                    "placeholder": "Tên của bạn (Bắt buộc)",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "id": "phone",
                    "class": "form-control",
                    "placeholder": "Số điện thoại (Bắt buộc)",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "id": "email",
                    "class": "form-control",
                    "placeholder": "Email (Không bắt buộc)",
                    "required": False,
                }
            ),
            "facebook": forms.TextInput(
                attrs={
                    "id": "facebook",
                    "class": "form-control",
                    "placeholder": "Link Facebook (Không bắt buộc)",
                    "required": False,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "id": "message",
                    "placeholder": "Lời nhắn gửi đến đôi tình nhân",
                }
            ),
            "wedding": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "wedding",
                    "style": "display: None",
                }
            ),
        }
