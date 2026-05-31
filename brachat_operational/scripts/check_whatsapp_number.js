// check_whatsapp_number.js
// Executa este script com `node check_whatsapp_number.js` para imprimir o número de WhatsApp configurado.

const fs = require('fs');
const yaml = require('js-yaml');
const path = require('path');

const configPath = path.resolve(__dirname, '../config.yaml');

try {
  const file = fs.readFileSync(configPath, 'utf8');
  const config = yaml.load(file);
  if (config.whatsapp && config.whatsapp.enabled) {
    console.log('WhatsApp está habilitado. Número configurado:');
    console.log(config.whatsapp.number);
  } else {
    console.log('WhatsApp não está habilitado na configuração.');
  }
} catch (e) {
  console.error('Erro ao ler config.yaml:', e.message);
}
