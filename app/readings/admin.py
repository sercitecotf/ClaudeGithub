from django.contrib import admin

from .models import Elemento, Lectura


@admin.register(Elemento)
class ElementoAdmin(admin.ModelAdmin):
    list_display = ["categoria", "nombre", "activo"]
    list_filter = ["categoria", "activo"]
    search_fields = ["nombre", "categoria"]


@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    list_display = [
        "fecha",
        "elemento",
        "control_point",
        "valor_numerico",
        "valor_booleano",
        "dentro_de_rango",
        "registrado_por",
    ]
    list_filter = ["control_point__categoria", "elemento__categoria", "fecha"]
    search_fields = ["elemento__nombre", "control_point__nombre"]
    autocomplete_fields = ["control_point", "elemento"]
    readonly_fields = ["registrado_por", "creado_en"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)
