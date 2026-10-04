"""A4 Orquestador: máquina de estados que impone por código las firmas A2/A3/OWNER."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from .a1_creador import Creador
from .a2_supervisor import Supervisor
from .a3_seguridad import Seguridad
from .models import Borrador, Caso, Hallazgo, hash_texto

MAX_ITERACIONES_ECC = 3


class Estado(str, Enum):
    RECIBIDO = "RECIBIDO"
    REDACTADO = "REDACTADO"
    VALIDADO_QA = "VALIDADO_QA"
    VALIDADO_SEG = "VALIDADO_SEG"
    APROBADO_PROPIETARIO = "APROBADO_PROPIETARIO"
    ENVIADO = "ENVIADO"
    ESCALADO = "ESCALADO"    # terminal hasta decisión humana
    BLOQUEADO = "BLOQUEADO"  # terminal: veto de seguridad


_TRANSICIONES = {
    Estado.RECIBIDO: {Estado.REDACTADO, Estado.BLOQUEADO},
    Estado.REDACTADO: {Estado.VALIDADO_QA, Estado.ESCALADO},
    Estado.VALIDADO_QA: {Estado.VALIDADO_SEG, Estado.BLOQUEADO},
    # Sin aprobación necesaria se pasa directo a ENVIADO.
    Estado.VALIDADO_SEG: {Estado.APROBADO_PROPIETARIO, Estado.ENVIADO, Estado.REDACTADO},
    # El propietario puede editar el texto: se reabre el ciclo.
    Estado.APROBADO_PROPIETARIO: {Estado.ENVIADO, Estado.REDACTADO},
    Estado.ENVIADO: set(), Estado.ESCALADO: set(), Estado.BLOQUEADO: set(),
}


class TransicionInvalida(Exception):
    pass


@dataclass
class _Expediente:
    caso: Caso
    estado: Estado = Estado.RECIBIDO
    borrador: Borrador | None = None
    iteracion: int = 0
    firmas: dict[str, str | None] = field(
        default_factory=lambda: {"A2": None, "A3": None, "OWNER": None})
    propietario_pendiente: bool = False
    enviado: str | None = None


class Orquestador:
    def __init__(self, creador: Creador, supervisor: Supervisor, seguridad: Seguridad,
                 gateway: Callable[[str, str], None] | None = None):
        self._a1, self._a2, self._a3 = creador, supervisor, seguridad
        self._gateway = gateway or (lambda case_id, texto: None)
        self.casos: dict[str, _Expediente] = {}
        self.auditoria: list[dict] = []  # append-only, encadenada por hash

    # ---- API pública -------------------------------------------------
    def recibir(self, caso: Caso) -> Estado:
        exp = self.casos[caso.case_id] = _Expediente(caso)
        self._log(exp, "RECIBIDO", "caso recibido")
        pre = self._a3.pre_chequeo(caso.mensaje)
        if pre.veredicto == "BLOQUEADO":
            self._mover(exp, Estado.BLOQUEADO, f"pre-chequeo A3: {_cod(pre.hallazgos)}")
            return exp.estado
        return self._avanzar(exp)

    def aprobar(self, case_id: str, texto_final: str | None = None) -> Estado:
        """Firma de José Ángel. Si edita el texto, se repite QA y seguridad."""
        exp = self.casos[case_id]
        if not exp.propietario_pendiente or exp.estado is not Estado.VALIDADO_SEG:
            raise TransicionInvalida("el caso no espera aprobación del propietario")
        exp.propietario_pendiente = False
        if texto_final is not None and hash_texto(texto_final) != exp.firmas["A2"]:
            exp.borrador.texto = texto_final
            exp.firmas = {"A2": None, "A3": None, "OWNER": None}
            exp.propietario_pendiente = True  # la aprobación ya está dada
            self._mover(exp, Estado.REDACTADO, "texto editado por el propietario")
            exp.iteracion = MAX_ITERACIONES_ECC - 1  # sin reescritura por A1
            return self._validar(exp, owner_ok=True)
        exp.firmas["OWNER"] = exp.firmas["A2"]
        self._mover(exp, Estado.APROBADO_PROPIETARIO, "aprobado por José Ángel")
        return self._enviar(exp)

    def rechazar(self, case_id: str) -> Estado:
        exp = self.casos[case_id]
        exp.propietario_pendiente = False
        self._mover(exp, Estado.ESCALADO, "rechazado por el propietario")
        return exp.estado

    # ---- flujo interno -----------------------------------------------
    def _avanzar(self, exp: _Expediente) -> Estado:
        correcciones: list[Hallazgo] = []
        while True:
            exp.borrador = self._a1.redactar(exp.caso, correcciones)
            self._mover(exp, Estado.REDACTADO, f"borrador A1 (iteración {exp.iteracion})")
            qa = self._a2.revisar(exp.borrador)
            if qa.veredicto == "APROBADO":
                break
            exp.iteracion += 1
            self._log(exp, "QA_RECHAZADO", _cod(qa.hallazgos))
            if exp.iteracion >= MAX_ITERACIONES_ECC:
                self._mover(exp, Estado.ESCALADO, "ECC sin convergencia en 3 iteraciones")
                return exp.estado
            correcciones = qa.hallazgos
        return self._validar(exp, owner_ok=False, qa=qa)

    def _validar(self, exp: _Expediente, owner_ok: bool, qa=None) -> Estado:
        qa = qa or self._a2.revisar(exp.borrador)
        if qa.veredicto != "APROBADO":
            self._mover(exp, Estado.ESCALADO, f"QA tras edición: {_cod(qa.hallazgos)}")
            return exp.estado
        exp.firmas["A2"] = qa.hash_texto
        self._mover(exp, Estado.VALIDADO_QA, "firma A2")
        sec = self._a3.revisar_salida(exp.borrador.texto, exp.caso)
        if sec.veredicto != "SEGURO":
            exp.firmas["A2"] = None
            self._mover(exp, Estado.BLOQUEADO, f"veto A3: {_cod(sec.hallazgos)}")
            return exp.estado
        exp.firmas["A3"] = sec.hash_texto
        self._mover(exp, Estado.VALIDADO_SEG, "firma A3")
        if exp.borrador.tiene_precio or exp.caso.canal == "seo":
            if owner_ok:
                exp.firmas["OWNER"] = qa.hash_texto
                self._mover(exp, Estado.APROBADO_PROPIETARIO, "aprobado por José Ángel")
                return self._enviar(exp)
            exp.propietario_pendiente = True
            self._log(exp, "PENDIENTE_PROPIETARIO", "esperando aprobación de José Ángel")
            return exp.estado
        return self._enviar(exp)

    def _enviar(self, exp: _Expediente) -> Estado:
        texto = exp.borrador.texto
        h = hash_texto(texto)
        necesita_owner = exp.borrador.tiene_precio or exp.caso.canal == "seo"
        requeridas = ["A2", "A3"] + (["OWNER"] if necesita_owner else [])
        if any(exp.firmas[k] != h for k in requeridas):  # control técnico, no de prompt
            raise TransicionInvalida("firmas ausentes o no coinciden con el texto final")
        self._gateway(exp.caso.case_id, texto)
        exp.enviado = texto
        self._mover(exp, Estado.ENVIADO, "enviado")
        return exp.estado

    def _mover(self, exp: _Expediente, destino: Estado, motivo: str) -> None:
        if destino is not exp.estado and destino not in _TRANSICIONES[exp.estado]:
            raise TransicionInvalida(f"{exp.estado.value} → {destino.value}")
        exp.estado = destino
        self._log(exp, destino.value, motivo)

    def _log(self, exp: _Expediente, evento: str, motivo: str) -> None:
        prev = self.auditoria[-1]["hash"] if self.auditoria else ""
        entrada = {"case_id": exp.caso.case_id, "evento": evento, "motivo": motivo,
                   "prev": prev}
        entrada["hash"] = hashlib.sha256(
            json.dumps(entrada, sort_keys=True).encode()).hexdigest()
        self.auditoria.append(entrada)


def _cod(hallazgos) -> str:
    return ", ".join(h.codigo for h in hallazgos) or "-"
