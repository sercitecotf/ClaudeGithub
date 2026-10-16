from django.urls import path

from . import views

app_name = "control_points"

urlpatterns = [
    path("", views.ControlPointListView.as_view(), name="list"),
    path("<int:pk>/", views.ControlPointDetailView.as_view(), name="detail"),
]
