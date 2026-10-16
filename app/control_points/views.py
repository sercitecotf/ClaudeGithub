from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import ControlPoint


class ControlPointListView(LoginRequiredMixin, ListView):
    model = ControlPoint
    paginate_by = 20
    context_object_name = "control_points"
    template_name = "control_points/controlpoint_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("categoria")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(
                Q(objeto__icontains=query)
                | Q(nombre__icontains=query)
                | Q(categoria__nombre__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class ControlPointDetailView(LoginRequiredMixin, DetailView):
    model = ControlPoint
    context_object_name = "control_point"
    template_name = "control_points/controlpoint_detail.html"
