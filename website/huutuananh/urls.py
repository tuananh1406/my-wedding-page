"""huutuananh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import include, path


def trigger_error(request):
    """Kiểm tra thử thiết lập của Sentry"""
    result = 1 / 0
    return (result, request)


def healthcheck(request):
    "Healthcheck"
    return HttpResponse("HEALTHCHECK/", content_type="text/plain", status=200)


urlpatterns = [
    # Kiểm tra thiết lập Sentry
    path("sentry-debug/", trigger_error),
    # Đường dẫn của ứng dụng bên thứ 3
    path("summernote/", include("django_summernote.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    # Đường dẫn của all_auth
    path("logout", LogoutView.as_view()),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls),
    ]
else:
    urlpatterns += [
        path("custom-admin-url", admin.site.urls),
    ]

if not settings.IS_INSTALLING:
    urlpatterns += [
        # Đường dẫn của ứng dụng cá nhân
        path("weddings/", include("weddings.urls")),
        path("custom/", include("custom.urls")),
    ]
