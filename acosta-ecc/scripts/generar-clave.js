// Genera una clave de cifrado de 256 bits para ACOSTA_CLAVE.
console.log(require('crypto').randomBytes(32).toString('hex'));
