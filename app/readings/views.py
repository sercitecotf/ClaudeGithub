from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from control_points.models import Categoria

from .models import Lectura


class LecturaMonthListView(LoginRequiredMixin, ListView):
    """
    Lista de lecturas de un mes para una categoría de punto de control
    (Temperatura, Agua, Limpieza, ...), agrupadas por día y por elemento —
    equivalente a las pantallas "Lista de Reportes de Temperatura/Agua/..."
    de Qualitus.

    Nota: Qualitus usa un calendario interactivo (FullCalendar, con drag y
    colores). Esta primera versión es una tabla agrupada por día, más simple
    de construir y de probar; la interacción tipo calendario puede añadirse
    después sin cambiar el modelo de datos.
    """

    model = Lectura
    context_object_name = "lecturas"
    template_name = "readings/lectura_month_list.html"

    def dispatch(self, request, *args, **kwargs):
        self.categoria = get_object_or_404(Categoria, nombre__iexact=kwargs["categoria"])
        today = date.today()
        try:
            self.year = int(request.GET.get("year", today.year))
            self.month = int(request.GET.get("month", today.month))
        except ValueError:
            raise Http404("Año o mes inválido.")
        if not (1 <= self.month <= 12):
            raise Http404("Mes inválido.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            Lectura.objects.filter(
                control_point__categoria=self.categoria,
                fecha__year=self.year,
                fecha__month=self.month,
            )
            .select_related("elemento", "control_point")
            .order_by("fecha", "elemento__categoria", "elemento__nombre")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dias = {}
        for lectura in context["lecturas"]:
            dias.setdefault(lectura.fecha, []).append(lectura)

        context["categoria"] = self.categoria
        context["dias"] = sorted(dias.items())
        context["year"] = self.year
        context["month"] = self.month
        # Día 1 solo para poder formatear "mes año" en español con el
        # filtro `date` de Django, en vez de `calendar.month_name` (en inglés).
        context["month_reference"] = date(self.year, self.month, 1)

        prev_month = self.month - 1 or 12
        prev_year = self.year - 1 if self.month == 1 else self.year
        next_month = self.month + 1 if self.month < 12 else 1
        next_year = self.year + 1 if self.month == 12 else self.year
        context["prev_year"], context["prev_month"] = prev_year, prev_month
        context["next_year"], context["next_month"] = next_year, next_month
        return context
