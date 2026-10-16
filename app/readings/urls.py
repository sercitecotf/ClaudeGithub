from django.urls import path

from . import views

app_name = "readings"

urlpatterns = [
    path("<str:categoria>/", views.LecturaMonthListView.as_view(), name="month_list"),
]
