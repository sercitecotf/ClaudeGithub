# Análisis de Qualitus (surpan.qualitus.com)

Objetivo: entender la aplicación en producción, sin soporte del proveedor, para
construir un reemplazo propio. Análisis hecho sobre lo que entrega el servidor
públicamente: la página de login y el bundle de JavaScript/CSS de la interfaz
(`application-*.js` y `application-*.css` servidos por el asset pipeline de
Rails). No se usaron credenciales ni se accedió a datos de ningún usuario.

## Requisito para la reconstrucción: maestros desde SAP Business One

Decisión del usuario (no es parte del análisis de Qualitus, es un requisito
para la app nueva): los datos maestros — **Productos / Fichas de Producto** y
**Materias Primas**, y probablemente **Proveedores** — no se van a gestionar
dentro de la app nueva. Se van a traer de **SAP Business One**, por
**Service Layer** (API REST/OData que expone SAP B1 cuando corre sobre
HANA; también existe para B1 clásico en versiones recientes).

Esto cambia el modelo de datos respecto al Qualitus actual: ahí Proveedores
y Fichas de Producto son tablas propias, con su propio formulario de alta.
En la app nueva, esas pantallas pasan de **CRUD propio** a una
**vista de solo lectura sobre una caché sincronizada de SAP B1** (o una
consulta directa a Service Layer en el momento, si la latencia y el volumen
lo permiten). Las entidades típicas de Service Layer para esto son:

- `BusinessPartners` → Proveedores (filtrando por `CardType = 'S'`,
  suppliers).
- `Items` → Materias Primas y/o Productos (según cómo esté modelado en su
  SAP: puede que materia prima y producto terminado sean el mismo tipo de
  `Item` con un `ItemsGroupCode` distinto, o `U_` campos propios/UDF para
  distinguir).

Lo que seguiría siendo propio de la app nueva (no de SAP): el resto del
dominio APPCC — auditorías, puntos de control, inspecciones, no
conformidades, mantenimiento, temperatura, tareas, documentos IFS — porque
SAP B1 no modela nada de eso.

### Preguntas abiertas antes de diseñar la integración

No se puede cerrar el diseño de esta integración sin saber:

1. **Versión/hosting de SAP B1**: ¿on-premise, Cloud, sobre HANA o SQL
   Server? Service Layer requiere HANA (o B1 reciente sobre SQL con Service
   Layer habilitado); si es una versión vieja solo con DI API, habría que
   revisar esto.
2. **¿Service Layer ya está habilitado y accesible** desde donde correrá la
   app nueva (red, certificado, usuario de integración con los permisos
   mínimos necesarios)?
3. **Campos personalizados (UDF/UDT)** en `Items` y `BusinessPartners` que la
   app nueva necesite mostrar (p. ej. categoría de proveedor como la que ya
   usa Qualitus, alérgenos, etc.) — si existen, hay que mapearlos.
4. **Tiempo real vs. sincronización periódica**: ¿cada pantalla consulta
   Service Layer al vuelo, o se sincroniza a una tabla local cada cierto
   tiempo (más rápido de mostrar, pero con desfase)? Para listados con
   cientos de proveedores o ítems, lo normal es cachear y refrescar
   periódicamente, no consultar Service Layer en cada carga de página.
5. **Dirección de la sincronización**: ¿la app nueva solo lee de SAP, o en
   algún caso necesita escribir de vuelta (p. ej. marcar un proveedor como
   "aprobado" en la app y que eso se refleje en SAP)? Si es solo lectura,
   la integración es mucho más simple.

## Qué es la aplicación

Captura del panel principal (aportada por el usuario, ya autenticado) confirma
que es un sistema de **gestión de calidad e inocuidad alimentaria (tipo
APPCC/HACCP)**, con estos módulos en el menú:

Proveedores · Agua · Puntos de Control · Materias Primas · Limpieza ·
Auditorías · Fichas de Producto · Mantenimiento · Inspecciones · Compras ·
Temperatura · No Conformidades · Producción · Grupos de Trabajo · Análisis ·
Inventario · Plagas · Tareas · Expediciones · Residuos · Documentos de
Certificación.

Pie de página: "Copyright © 2012-2016 Qualitus". La marca de tiempo del
copyright y el stack (ver abajo) sugieren una aplicación Rails con varios años
sin actualizar en el frontend.

## Stack técnico identificado

Del `<head>` de la página de login (`login-page.html`) y del propio bundle:

- **Backend:** Ruby on Rails (asset pipeline / Sprockets, rutas `/users/sign_in`,
  `/users/password/new`, formularios generados con el patrón de **SimpleForm**
  `authenticity_token`/`utf8` de Rails, gema **Devise** para autenticación por
  las rutas `users/...`).
- **Frontend:**
  - jQuery 3.5.1 (CDN de Google), jQuery UI (datepicker, dialog, menu, slider,
    spinner).
  - Bootstrap 3 (`navbar`, `btn`, clases `.form-group`).
  - **select2** para selects con búsqueda.
  - **FullCalendar** (con locale `es`) para calendarios de tareas e informes.
  - **Dygraph** para gráficos de series temporales — probablemente el módulo
    de Temperatura.
  - **FilePond** (+ plugin `FilePondPluginImagePreview`) para subir archivos,
    incluyendo advertencia de tamaño para vídeos (>50 MB).
  - **jsTree** con plugin `checkbox` para el árbol de permisos por rol
    (`#permissions`).
  - **BootstrapDialog** para modales de confirmación y vistas rápidas.
  - **fabric.js** y **tui-image-editor** (+ `tui-color-picker`) para anotar o
    editar imágenes (probablemente evidencia fotográfica de inspecciones o
    no conformidades).
  - Un plugin propio `doubleScroll` (scrollbar superior sincronizada, para
    tablas anchas).
  - Patrón **cocoon** (gema Rails) para formularios anidados dinámicos: se ve
    en los eventos `cocoon:after-insert` / `cocoon:after-remove` /
    `cocoon:before-remove` repetidos en casi todos los módulos.

## Mapa de dominio (del JS + del menú)

| Módulo del menú | Evidencia en el JS |
|---|---|
| **Tareas** | `onTaskCategoryChange`, clases `.task-fields` / `.specific-task-data`, calendario `.tasks-calendar` con `fullCalendar` |
| **Auditorías** | `#audit_category` (interno/externo), `#audit_items` con `.audit-requirements-select`, ruta `GET /audit_requirements/:id/pull` para traer la descripción del requisito |
| **Proveedores** | `#provider_provider_category_id`, `#provider_documents` (anidado con cocoon), `.provider-category-document`, `#provider_state` con `.provider_exception_reason` (estado de excepción) |
| **Compras** | `#purchase_provider_id`, `#purchase_components` (anidado), filtra componentes por proveedor con `data-provider` |
| **Fichas de Producto** | `#product_sheet_category`, `#product_sheet_stages` con `.stage-provider-components`, rutas `GET /components/load_xhr_data_components` y `GET /components/:id/load_xhr_data_component_providers` |
| **Puntos de Control** | `.masterControlPonts`, `.controllable-resource`, ruta `POST /report_control_points/store` |
| **Inspecciones** | `#inspection_category`, `#inspection_schedule`, `#inspection_places` (anidado), ruta `GET /places.json` y `GET /inspection_result_sets/new` (carga dinámica por AJAX con `dataType: "script"`, patrón `respond_to :js` de Rails) |
| **No Conformidades** | `#issue_issuable_type` / `#issue_issuable_id` — asociación polimórfica de Rails (`issuable_type` + `issuable_id`), ruta `GET /origins` según el tipo elegido |
| **Grupos de Trabajo / usuarios** | `.user_roles` → `GET /users/functionalities` (permisos dependientes del rol), árbol de permisos con jsTree, alta de empleados con usuario asociado o predefinido (`associate_user`, `predefined_user`) |
| **Temperatura** | Uso de Dygraph para series temporales; no se vio ruta específica en el HTML/JS público |
| **Agua, Limpieza, Mantenimiento, Producción, Inventario, Plagas, Expediciones, Residuos, Documentos de Certificación, Análisis** | Aparecen en el menú pero no dejaron rastro distintivo en el JS público; probablemente reutilizan los mismos patrones (formularios anidados cocoon, selects dependientes vía AJAX, archivos con FilePond) |

Un detalle reutilizable para el rediseño: casi todo módulo con sub-ítems (items
de auditoría, documentos de proveedor, componentes de ficha de producto,
lugares de inspección) usa el mismo patrón: **formulario anidado con cocoon +
select dependiente que dispara una petición AJAX que devuelve un fragmento de
JavaScript** (`dataType: "script"`, no JSON), típico de Rails UJS con vistas
`.js.erb`.

## Archivos guardados

- `login-page.html`: HTML de `/users/sign_in` (token CSRF y de formulario
  reemplazados por `[redacted]`).
- `js-bundle/application.pretty.js`: el bundle de JS de la interfaz,
  formateado para lectura (fuente: `application-9c5a50eb...js`, 1.1 MB
  minificado → 1.95 MB formateado, 36 759 líneas). Incluye todas las
  librerías de terceros además del código propio.
- `js-bundle/application.css`: hoja de estilos de la interfaz
  (`application-cd54ad3f...css`).

## Módulos confirmados con capturas de pantalla (sesión autenticada)

El usuario compartió capturas de 5 listados ya logueado. No se guardaron las
imágenes en el repo porque muestran datos reales (nombres de empleados,
auditores, emails, teléfonos y matrículas); aquí solo se documenta la
**estructura de campos**, con ejemplos genéricos en vez de los datos reales.

### Proveedores (`LISTA DE PROVEEDORES`)

Columnas: Código, Nombre (con la categoría del proveedor como subtítulo, p. ej.
"Laboratorio", "Mantenimiento", "Prov. Productos distribución"), Email,
Teléfono, Estado de Documentos (indicador en punto de color), Estado
(Pendiente / Aprobado), acciones **Contratos** y **Ver**. Paginado de 20 en 20
("Mostrando 1-20 de proveedores N en total"). Confirma lo que ya se veía en el
JS: `provider_provider_category_id` es la categoría mostrada como subtítulo, y
"Estado de Documentos" es el semáforo que depende de `#provider_documents` /
`.provider-category-document` (documentos requeridos según la categoría).

### Mantenimiento (`LISTA DE REPORTES DE MANTENIMIENTO`)

Columnas: Elemento (activo o equipo, p. ej. depósito, cuentalitros, horno),
Categoría (Preventivo / Verificación), Reportado por, Fecha de Reporte,
Verificado por, Fecha de Verificación, Estado (Verificado), Comentarios,
acción **Ver**; botón de exportar a **CSV**. Es un módulo separado de
"Puntos de Control", con su propio flujo de reporte → verificación por una
segunda persona. No se había visto rastro de este módulo en el JS público; es
un modelo nuevo a documentar (`maintenance_reports` o similar, con
`reported_by`, `verified_by`, `verified_at`, `comments`, categoría y elemento
asociado).

### Temperatura (`LISTA DE REPORTES DE TEMPERATURA`)

Vista de **calendario mensual** (no tabla), construida con FullCalendar (igual
que `.tasks-calendar` / `.reports-calendar` vistos en el JS, con
`lang: "es"`). Cada día agrupa entradas por categoría de elemento (p. ej.
cámaras de un obrador, vehículos de reparto) y, dentro de cada categoría, una
fila por elemento (matrícula o cámara). Esto confirma que el Dygraph incluido
en el bundle se usa en el **detalle** de cada reporte (gráfico de la serie de
temperatura), mientras que el listado usa calendario. También tiene
exportación a CSV.

### Puntos de Control (`LISTA DE PUNTOS DE CONTROL`)

Columnas: Objeto (ubicación/equipo, p. ej. "Obrador frío lavamanos 1"),
Categoría (p. ej. Agua), Nombre (p. ej. "Nivel de cloro libre", "Color",
"Sabor", "Olor", "Turbidez"), Tipo de Dato (**Numérico** / **Checkbox**, y por
el JS también **Texto**), Valor por Defecto, Valor Mínimo Aceptable, Valor
Máximo Aceptable, Texto por Defecto, Unidad de Medida, Requisito (Sí/No),
Crítico (Sí/No), acción **Ver**. 1352 registros en el entorno real. Esta
tabla es la confirmación directa del código visto antes en
`js-bundle/application.pretty.js` (función que muestra `.numeric-fields`,
`.boolean-fields` o `.text-fields` según el tipo de dato elegido): cada punto
de control es una definición de medición con tipo, rango aceptable y si es
crítico (esto es el corazón del modelo APPCC/HACCP — puntos críticos de
control).

### Auditorías (`LISTA DE AUDITORÍAS`)

Columnas: Tipo Auditoría (Externa / Interna), Fecha de Auditoría, Auditor,
Descripción (texto libre, en los ejemplos reales menciona normas como
ISO 9001:2015 e IFS), Estado (Cerrada), acción **Ver**. Pocas decenas de
registros. Confirma el `#audit_category` externo/interno visto en el JS.

### Inspecciones (`LISTA DE INSPECCIONES`)

Columnas: Nombre (título libre de la inspección, p. ej. "Control de Sala
Octubre" o el nombre de un contenedor/proveedor), Inspeccionado por, Fecha
Inspección, Verificado por, Fecha de Verificación, Categoría (p. ej. Proceso
productivo, Control de proveedores), Periodicidad (Diario, …), Estado
(Programado), acciones **Cerrar** y **Ver**; exportación a CSV. 1567
registros. Mismo patrón de doble firma que Mantenimiento (inspeccionado por /
verificado por), y confirma `#inspection_category` / `#inspection_schedule`
(periodicidad) ya vistos en el JS. El botón **Cerrar** sugiere un estado de
ciclo de vida (Programado → Cerrado) además de lo que ya se veía
(`inspection_result_sets`, lugares de inspección).

### No Conformidades (`LISTA DE NO CONFORMIDADES`)

Columnas: E.I. (icono de estado — visto en rojo/interrogación o verde/check,
probablemente "Evaluación de Impacto" o similar: abierta vs. resuelta),
ID, Categoría (Observación, Desviación), Descripción (texto libre), Origen
(enlace a "Inspección" — la asociación polimórfica `issuable_type` /
`issuable_id` vista en el JS, donde el origen también podría ser otro módulo
además de inspección), Fecha de Detección, Acciones Correctivas (Sí/No, con
icono de check cuando existen), acción **Ver**; buscador con **Búsqueda
Avanzada** desplegable y exportación a CSV. 1180 registros. Esto es el
módulo "No Conformidades" del menú principal, construido sobre lo que el JS
llama "issues" (`#issue_issuable_type`, `#issue_issuable_id`, `/origins`).

### Análisis (`LISTA DE ANÁLISIS`)

Columnas: Fecha de Solicitud, Nombre (solicitante, a veces vacío), Objeto de
Análisis (texto compuesto: tipo de reporte + elemento + fecha, p. ej.
"Reporte de Temperatura / <elemento> - <fecha>", "Reporte de Limpieza / …",
"Reporte de Agua / …"), Estado (Solicitado), acciones **Ver** y **Enviar
Resultados**. 17 registros. Confirma que "Análisis" no es un módulo
independiente con su propio dominio, sino una **cola de solicitudes de
laboratorio** que referencia reportes de otros módulos (Temperatura, Agua,
Limpieza) — el objeto analizado siempre es un reporte existente, no un dato
propio de Análisis.

### Tareas (`LISTA DE TAREAS`)

Igual que Temperatura, es un **calendario mensual/semanal/diario**
(FullCalendar, con selector Mes/Semana/Día) en vez de tabla. Cada celda es
una tarea con su categoría entre paréntesis (p. ej. "(MANTENIMIENTO)") y
color según estado/urgencia (verde completada, rojo pendiente o vencida, a
juzgar por el contraste). El texto de la tarea suele indicar el tipo
("CONTROL CLORO Y TEMPERATURA", "MANTENIMIENTO PREVENTIVO", "LIMPIEZA
MÁQUINA...") y a veces el responsable asignado. Esto confirma
`onTaskCategoryChange` y `.tasks-calendar` del JS: las tareas son genéricas
y su categoría decide qué campos del formulario mostrar
(`.specific-task-data`), y aquí se ve que categorías como Mantenimiento y
Limpieza generan tareas recurrentes automáticamente en el calendario.

### Documentos IFS (`LISTA DE DOCUMENTOS IFS`)

Columnas: Categoría (p. ej. "Responsabilidad de la dirección", "Sistema de
gestión de la calidad y la seguridad alimentaria", "Gestión de los
recursos"), Código IFS, Código BRC, Nombre, Descripción, acción **Ver**. 44
registros. Es el catálogo de "Documentos de Certificación" del menú
principal: cada documento interno de la empresa (política, manual de
calidad, procedimientos) está mapeado a los puntos de las normas de
certificación alimentaria **IFS Food** y **BRC**, con numeración de ambas
normas en paralelo.

## Límites del análisis

- Solo se analizó lo que el servidor entrega sin autenticación (login +
  assets estáticos). No se inició sesión ni se exploraron datos ni rutas que
  requieran credenciales.
- El bundle de JS mezcla librerías y código propio en una sola pasada de
  minificación, así que no hay una separación limpia por archivo original;
  la tabla de arriba identifica el código propio por los selectores y rutas
  específicas del dominio (`task-fields`, `inspection_category`, etc.), no por
  límites de archivo.
- Módulos del menú aún sin confirmar con capturas ni con código propio en el
  bundle: Agua, Limpieza, Producción, Inventario, Plagas, Residuos,
  Expediciones, Compras, Fichas de Producto, Grupos de Trabajo. Es probable
  que Agua y Limpieza no sean módulos independientes sino categorías dentro
  de "Puntos de Control" (se vio "Agua" como categoría ahí) y dentro de
  "Análisis" (se vio "Reporte de Limpieza" y "Reporte de Agua" como objetos
  de análisis), pero no se confirmó su propia pantalla de listado.
- Las capturas de pantalla que confirmaron Proveedores, Mantenimiento,
  Temperatura, Puntos de Control, Auditorías, Inspecciones, No Conformidades,
  Análisis, Tareas y Documentos IFS mostraban datos reales (nombres de
  empleados y auditores, emails, teléfonos, matrículas, nombres de
  clientes/proveedores, descripciones de incidentes). Esos datos no se
  guardaron en el repo; el documento solo describe la estructura de campos
  con ejemplos genéricos.
