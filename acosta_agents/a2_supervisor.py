"""A2 Supervisor ECC: audita el borrador de A1. Solo lectura, falla cerrado."""
from __future__ import annotations

import re
from decimal import Decimal

from .models import Borrador, Hallazgo, QAReport, hash_texto
from .sources import Catalogo, FuenteNoDisponible, Tarifario

_IMPORTE = re.compile(r"(\d+(?:[.,]\d{1,2})?)\s*€")
# Erratas frecuentes sin tilde (lista mínima; ampliar con la guía de estilo).
_ERRATAS = {"tecnico": "técnico", "presupuesto,": None, "garantia": "garantía",
            "telefono": "teléfono", "direccion": "dirección"}
_ERRATAS = {k: v for k, v in _ERRATAS.items() if v}
_PROMESAS = re.compile(r"\b(ahora mismo|en \d+ minutos|sin falta|garantizado)\b", re.I)


def _a_decimal(s: str) -> Decimal:
    return Decimal(s.replace(",", "."))


class Supervisor:
    def __init__(self, cargar_tarifario=Tarifario, cargar_catalogo=Catalogo):
        self._cargar_tarifario = cargar_tarifario
        self._cargar_catalogo = cargar_catalogo

    def revisar(self, borrador: Borrador) -> QAReport:
        h = hash_texto(borrador.texto)
        try:
            tarifario, catalogo = self._cargar_tarifario(), self._cargar_catalogo()
        except FuenteNoDisponible as e:  # fail-closed
            return QAReport("RECHAZADO", h, [Hallazgo(
                "FUENTE_NO_DISPONIBLE", "BLOQUEANTE", f"No se puede verificar: {e}")])

        f: list[Hallazgo] = []
        # [P] Precios
        for p in borrador.precios_usados:
            oficial = tarifario.importe(p.id_tarifa)
            if oficial is None:
                f.append(Hallazgo("P_ID_INVALIDO", "BLOQUEANTE",
                                  f"id_tarifa inexistente: {p.id_tarifa}"))
            elif oficial != p.importe:
                f.append(Hallazgo("P_IMPORTE", "BLOQUEANTE",
                                  f"{p.id_tarifa}: {p.importe} ≠ tarifario {oficial}"))
        permitidos = {p.importe for p in borrador.precios_usados}
        total = sum(permitidos, Decimal(0))
        for m in _IMPORTE.findall(borrador.texto):
            if _a_decimal(m) not in permitidos | {total}:
                f.append(Hallazgo("P_IMPORTE_EN_TEXTO", "BLOQUEANTE",
                                  f"Importe {m} € del texto sin id_tarifa que lo respalde"))
        # [T] Viabilidad técnica
        if borrador.servicio_id is not None:
            visita = catalogo.requiere_visita(borrador.servicio_id)
            if visita is None:
                f.append(Hallazgo("T_FUERA_DE_CATALOGO", "BLOQUEANTE",
                                  f"Servicio no catalogado: {borrador.servicio_id}"))
            elif visita and (borrador.precios_usados or _IMPORTE.search(borrador.texto)):
                f.append(Hallazgo("T_PRECIO_SIN_VISITA", "BLOQUEANTE",
                                  "Precio cerrado en un trabajo que requiere visita"))
            elif catalogo.servicios[borrador.servicio_id].get("requiere_titularidad") and \
                    "REQUIERE_VERIFICACION_TITULARIDAD" not in borrador.flags:
                f.append(Hallazgo("T_TITULARIDAD", "MAYOR",
                                  "Falta verificación de titularidad en la apertura"))
        # [E] Estilo y ortografía
        for mal, bien in _ERRATAS.items():
            if re.search(rf"\b{mal}\b", borrador.texto, re.I):
                f.append(Hallazgo("E_ORTOGRAFIA", "MENOR", f"'{mal}' → '{bien}'"))
        # [V] Veracidad
        if _PROMESAS.search(borrador.texto):
            f.append(Hallazgo("V_PROMESA", "MAYOR",
                              "Promesa de plazo/garantía no confirmada por el orquestador"))

        bloquea = any(x.severidad in ("BLOQUEANTE", "MAYOR") for x in f)
        return QAReport("RECHAZADO" if bloquea else "APROBADO", h, f)
