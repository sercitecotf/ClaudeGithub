// Páginas legales generadas desde data/empresa.json. Si falta un dato (solo posible en desarrollo)
// se muestra resaltado; en producción el servidor no arranca con datos legales incompletos.
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const val = (x) => (x && String(x).trim() ? esc(x) : '<span class="todo">COMPLETAR</span>');

const page = (title, body) => `<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Soldadura Acosta La Palma</title><meta name="robots" content="noindex">
<link rel="icon" href="/img/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="/css/site.css"></head>
<body><header class="site"><div class="wrap">
<a class="brand" href="/"><img src="/img/mark.svg" alt="" width="46" height="46"><span class="brand-text"><b>Soldadura Acosta</b><small>La Palma · Cerrajería y metal</small></span></a>
<a class="btn btn-fire" href="/" style="min-height:44px">Volver a la web</a></div></header>
<main class="legal"><section><div class="wrap"><h1>${esc(title)}</h1>${body}</div></section></main></body></html>`;

const titular = (e) => `<ul>
<li>Titular: ${val(e.titular)} (${val(e.nombre_comercial)})</li>
<li>NIF: ${val(e.nif)}</li>
<li>Domicilio: ${val(e.domicilio)}</li>
<li>Teléfono: ${val(e.telefono)}</li>
<li>Correo electrónico: ${val(e.email)}</li>
<li>Dominios: ${(e.dominios || []).map(esc).join(' · ')}</li></ul>`;

function avisoLegal(e) {
  return page('Aviso legal', `
<h2>Titular del sitio web</h2>${titular(e)}
<h2>Objeto</h2><p>Este sitio web ofrece información sobre los servicios de cerrajería, soldadura a medida, carpintería metálica y reparaciones de urgencia de ${val(e.nombre_comercial)}, y permite solicitar presupuesto.</p>
<h2>Presupuestos y precios</h2><p>La información de la web tiene carácter orientativo. Los precios definitivos se confirman en el presupuesto, que en trabajos a medida puede requerir una visita previa para tomar medidas.</p>
<h2>Propiedad intelectual</h2><p>Los textos, el logotipo y las imágenes de este sitio son propiedad del titular o se utilizan con autorización. Queda prohibida su reproducción sin permiso.</p>
<h2>Legislación aplicable</h2><p>Este aviso se rige por la legislación española. Para cualquier controversia, las partes se someterán a los juzgados y tribunales que correspondan conforme a la normativa vigente.</p>`);
}

function privacidad(e) {
  return page('Política de privacidad', `
<h2>1. Responsable del tratamiento</h2>${titular(e)}
<h2>2. Qué datos tratamos y para qué</h2><p>Cuando nos escribes por el formulario, WhatsApp o teléfono tratamos tu nombre, teléfono, municipio, la dirección si nos la facilitas y los detalles del trabajo. Los usamos únicamente para <b>responder a tu solicitud, elaborar el presupuesto y prestar el servicio</b>.</p>
<h2>3. Base jurídica</h2><p>Tu consentimiento al enviar el formulario y la aplicación de medidas precontractuales a petición tuya (art. 6.1.a y 6.1.b del RGPD). Si contratas el servicio, también el cumplimiento del contrato y de las obligaciones legales (fiscales y de facturación).</p>
<h2>4. Asistente automatizado</h2><p>Para atender las solicitudes usamos un asistente automatizado. Los datos identificativos se sustituyen por códigos internos antes de que el asistente los procese y <b>ninguna oferta o presupuesto se envía sin la revisión y aprobación de ${val(e.titular)}</b>. No tomamos decisiones únicamente automatizadas con efectos jurídicos sobre ti.</p>
<h2>5. Seguridad</h2><p>Las solicitudes se almacenan cifradas. Los avisos internos de nueva solicitud no incluyen datos personales. No solicitamos ni tratamos datos bancarios por la web, el formulario ni el chat: el pago se realiza en persona al finalizar el trabajo.</p>
<h2>6. Destinatarios</h2><p>No cedemos tus datos a terceros salvo obligación legal. Presta servicios de alojamiento web, como encargado del tratamiento: ${val(e.proveedor_alojamiento)}.</p>
<h2>7. Conservación</h2><p>Conservamos los datos de las solicitudes durante ${val(e.retencion_confirmada ? e.retencion_meses : null)} meses desde su recepción, salvo que se convierta en un trabajo contratado, en cuyo caso se conservan el tiempo exigido por la normativa fiscal y mercantil.</p>
<h2>8. Tus derechos</h2><p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a ${val(e.email)}. Si consideras que tus derechos no han sido atendidos, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" rel="noopener">www.aepd.es</a>).</p>
<h2>9. Cookies</h2><p>Este sitio no utiliza cookies de seguimiento ni de publicidad, ni carga fuentes o recursos de terceros.</p>`);
}

module.exports = { avisoLegal, privacidad };
