"""Contratos de datos compartidos por los agentes."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from decimal import Decimal


def hash_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class PrecioUsado:
    concepto: str
    id_tarifa: str
    importe: Decimal


@dataclass
class Caso:
    case_id: str
    canal: str  # whatsapp | web | seo
    mensaje: str  # ya saneado y tokenizado por la pasarela
    urgencia: str = "BAJA"  # BAJA | MEDIA | ALTA | EMERGENCIA
    servicio_id: str | None = None
    pii_tokens: tuple[str, ...] = ()


@dataclass
class Borrador:
    texto: str
    precios_usados: list[PrecioUsado] = field(default_factory=list)
    servicio_id: str | None = None
    flags: list[str] = field(default_factory=list)

    @property
    def tiene_precio(self) -> bool:
        return any(p.importe > 0 for p in self.precios_usados)


@dataclass(frozen=True)
class Hallazgo:
    codigo: str
    severidad: str  # BLOQUEANTE | MAYOR | MENOR
    problema: str


@dataclass
class QAReport:
    veredicto: str  # APROBADO | RECHAZADO
    hash_texto: str
    hallazgos: list[Hallazgo] = field(default_factory=list)


@dataclass
class SecReport:
    veredicto: str  # SEGURO | BLOQUEADO
    riesgo: str  # BAJO | MEDIO | ALTO | CRITICO
    hash_texto: str
    hallazgos: list[Hallazgo] = field(default_factory=list)
