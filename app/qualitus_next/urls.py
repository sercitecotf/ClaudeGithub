from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("puntos-de-control/", include("control_points.urls")),
    path("lecturas/", include("readings.urls")),
    path("", RedirectView.as_view(pattern_name="control_points:list", permanent=False)),
]
