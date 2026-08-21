from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin-asmae/", admin.site.urls),
    path("", include("boucherie.urls")),
]