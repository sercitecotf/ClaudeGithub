# ClaudeGithub · Orquestador multi-agente (Soldadura Acosta La Palma)

Esqueleto del ecosistema ECC: A4 Orquestador con máquina de estados
`RECIBIDO → REDACTADO → VALIDADO_QA → VALIDADO_SEG → APROBADO_PROPIETARIO → ENVIADO`
(más `ESCALADO` y `BLOQUEADO`), y los agentes A1 Creador, A2 Supervisor y A3 Seguridad como módulos en `acosta_agents/`.

- El gateway solo envía si las firmas A2 y A3 (y OWNER en presupuestos y SEO) coinciden con el hash del texto final. Se impone en código.
- Bucle ECC máximo de 3 iteraciones; después se escala a José Ángel.
- `data/tarifario.json` y `data/catalogo_servicios.json` son fuentes de solo lectura. Los valores actuales son de **ejemplo** y deben ser validados por José Ángel.
- A1 admite un generador inyectable para conectar un LLM; por defecto usa una plantilla determinista.

Pruebas: `python3 -m pip install pytest && python3 -m pytest`
