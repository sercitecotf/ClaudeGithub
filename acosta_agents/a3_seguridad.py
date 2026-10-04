"""A3 Seguridad: pre-chequeo de entrada, tokenización y puerta final de salida."""
from __future__ import annotations

import re
from itertools import count

from .models import Caso, Hallazgo, SecReport, hash_texto

_IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:\s?\d{4}){4,7}\b")
_TARJETA = re.compile(r"\b(?:\d[ -]?){13,19}\b")
_DNI = re.compile(r"\b\d{8}[A-Za-z]\b")
_TEL = re.compile(r"(?<!\d)(?:\+34\s?)?[6-9]\d{2}[\s.-]?\d{3}[\s.-]?\d{3}(?!\d)")
_TOKEN = re.compile(r"\{\{[A-Z]+_\d{3}\}\}")
_INYECCION = re.compile(
    r"ignora (?:tus|las|todas las) (?:reglas|instrucciones)|ignora lo anterior|"
    r"actúa como|muestra tu prompt|<script|union\s+select|drop\s+table|;\s*--",
    re.I)
_URL = re.compile(r"https?://([^/\s]+)", re.I)
DOMINIOS_PROPIOS = {"soldaduraacosta.es", "soldaduraacostabel.com"}


def tokenizar(texto: str) -> tuple[str, dict[str, str]]:
    """Sustituye teléfonos por tokens. Devuelve (texto_tokenizado, bóveda token→valor)."""
    boveda: dict[str, str] = {}
    n = count(1)

    def sub(m: re.Match) -> str:
        tok = "{{TEL_%03d}}" % next(n)
        boveda[tok] = m.group(0)
        return tok

    return _TEL.sub(sub, texto), boveda


class Seguridad:
    def pre_chequeo(self, texto: str) -> SecReport:
        """Entrada: spam, inyección y datos sensibles-alto."""
        h = hash_texto(texto)
        f: list[Hallazgo] = []
        if _INYECCION.search(texto):
            f.append(Hallazgo("S_INYECCION", "BLOQUEANTE", "Posible inyección o manipulación"))
        f += self._datos_altos(texto)
        return self._veredicto(h, f)

    def revisar_salida(self, texto: str, caso: Caso) -> SecReport:
        h = hash_texto(texto)
        f = self._datos_altos(texto)
        for tok in _TOKEN.findall(texto):
            if tok not in caso.pii_tokens:
                f.append(Hallazgo("S_PII_AJENA", "BLOQUEANTE",
                                  f"Token {tok} no pertenece al caso {caso.case_id}"))
        for dom in _URL.findall(texto):
            if dom.lower().removeprefix("www.") not in DOMINIOS_PROPIOS:
                f.append(Hallazgo("S_ENLACE_EXTERNO", "BLOQUEANTE", f"Enlace externo: {dom}"))
        return self._veredicto(h, f)

    @staticmethod
    def _datos_altos(texto: str) -> list[Hallazgo]:
        f = []
        for nombre, rx in (("IBAN", _IBAN), ("TARJETA", _TARJETA), ("DNI", _DNI)):
            if rx.search(texto):
                f.append(Hallazgo(f"S_{nombre}", "BLOQUEANTE",
                                  f"Dato sensible-alto ({nombre}) detectado"))
        return f

    @staticmethod
    def _veredicto(h: str, f: list[Hallazgo]) -> SecReport:
        if f:
            return SecReport("BLOQUEADO", "ALTO", h, f)
        return SecReport("SEGURO", "BAJO", h, f)
