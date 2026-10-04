// Comprobación previa a publicar: npm run check
const { problems } = require('../src/config');
const { blockers, warnings } = problems();
console.log('\nSoldadura Acosta · comprobación antes de publicar\n');
if (!blockers.length) console.log('✔ Todo lo imprescindible está listo.\n');
blockers.forEach((b) => console.log(`✖ ${b}`));
warnings.forEach((w) => console.log(`! ${w}`));
console.log(blockers.length ? `\nFaltan ${blockers.length} cosa(s) imprescindible(s). No se puede publicar todavía.\n` : '\nListo para publicar.\n');
process.exit(blockers.length ? 1 : 0);
