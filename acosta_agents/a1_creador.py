"""A1 Creador: redacta borradores. Nunca envía y nunca inventa precios."""
from __future__ import annotations

from typing import Callable, Optional

from .models import Borrador, Caso, Hallazgo, PrecioUsado
from .sources import Catalogo, Tarifario

# Hook para conectar un LLM: (caso, instrucciones_de_correccion) -> Borrador
Generador = Callable[[Caso, list[Hallazgo]], Borrador]

# Conceptos del tarifario aplicables por servicio en el generador por defecto.
_TARIFAS_POR_SERVICIO = {"apertura_puerta": ["CER-APE-01"]}


class Creador:
    def __init__(self, tarifario: Tarifario, catalogo: Catalogo,
                 generador: Optional[Generador] = None):
        self._tarifario = tarifario
        self._catalogo = catalogo
        self._generador = generador or self._generador_por_defecto

    def redactar(self, caso: Caso, correcciones: list[Hallazgo] | None = None) -> Borrador:
        return self._generador(caso, correcciones or [])

    def _generador_por_defecto(self, caso: Caso, correcciones: list[Hallazgo]) -> Borrador:
        sid = caso.servicio_id
        if sid is None or self._catalogo.requiere_visita(sid) in (None, True):
            return Borrador(
                texto="Gracias por escribirnos. Lo consulto con José Ángel y le confirmamos "
                      "el precio tras valorar el trabajo. Será necesaria una visita.",
                servicio_id=sid, flags=["REQUIERE_VISITA"],
            )
        precios = []
        for id_t in _TARIFAS_POR_SERVICIO.get(sid, []):
            t = self._tarifario.tarifas[id_t]
            precios.append(PrecioUsado(t["concepto"], id_t, t["importe"]))
        lineas = "; ".join(f"{p.concepto}: {p.importe} €" for p in precios)
        return Borrador(
            texto=f"Presupuesto orientativo ({lineas}), IGIC no incluido. "
                  "Al llegar el técnico comprobará que vive en la vivienda (DNI o recibo).",
            precios_usados=precios, servicio_id=sid,
            flags=["REQUIERE_VERIFICACION_TITULARIDAD"],
        )
