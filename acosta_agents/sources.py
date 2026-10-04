"""Fuentes de verdad de solo lectura: tarifario.json y catalogo_servicios.json."""
from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from types import MappingProxyType

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class FuenteNoDisponible(Exception):
    """La fuente no existe o es ilegible; los consumidores deben fallar cerrado."""


def _leer(ruta: Path) -> dict:
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        raise FuenteNoDisponible(f"{ruta.name}: {e}") from e


class Tarifario:
    """Vista inmutable de tarifario.json. Nunca se escribe desde el código."""

    def __init__(self, ruta: Path | None = None):
        raw = _leer(ruta or DATA_DIR / "tarifario.json")
        self.igic = Decimal(str(raw["igic"]))
        self.tarifas = MappingProxyType(
            {
                id_: MappingProxyType(
                    {"concepto": t["concepto"], "importe": Decimal(str(t["importe"]))}
                )
                for id_, t in raw["tarifas"].items()
            }
        )

    def importe(self, id_tarifa: str) -> Decimal | None:
        t = self.tarifas.get(id_tarifa)
        return t["importe"] if t else None


class Catalogo:
    """Vista inmutable de catalogo_servicios.json."""

    def __init__(self, ruta: Path | None = None):
        raw = _leer(ruta or DATA_DIR / "catalogo_servicios.json")
        self.servicios = MappingProxyType(
            {s["id"]: MappingProxyType(s) for s in raw["servicios"]}
        )

    def requiere_visita(self, servicio_id: str) -> bool | None:
        s = self.servicios.get(servicio_id)
        return None if s is None else bool(s.get("requiere_visita"))
