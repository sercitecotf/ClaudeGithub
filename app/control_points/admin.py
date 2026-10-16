from django.contrib import admin

from .models import Categoria, ControlPoint


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]


@admin.register(ControlPoint)
class ControlPointAdmin(admin.ModelAdmin):
    list_display = [
        "objeto",
        "categoria",
        "nombre",
        "tipo_dato",
        "unidad_medida",
        "requisito",
        "critico",
    ]
    list_filter = ["categoria", "tipo_dato", "requisito", "critico"]
    search_fields = ["objeto", "nombre"]
    autocomplete_fields = ["categoria"]
