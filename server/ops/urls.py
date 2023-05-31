from django.urls import path, re_path
from django.shortcuts import redirect

from .views import host

app_name = "ops"

urlpatterns = [path("rlock/", host.HostControlsView.as_view(), name="round_lock")]
