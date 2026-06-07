#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const numero = process.argv[2];
const texto = process.argv[3];
const remetente = process.argv[4] || 'nice';

if (!numero || !texto) {
  console.log('Uso: node queue.js NUMERO "TEXTO" [remetente]');
  console.log('Ex:  node queue.js 5561984128875 "Olá!" nice');
  process.exit(1);
}

const queueFile = path.join(__dirname, 'queue.json');
let queue = [];
try {
  queue = JSON.parse(fs.readFileSync(queueFile, 'utf-8'));
} catch {}

queue.push({
  to: numero,
  text: texto,
  from: remetente,
  status: 'pending',
  created_at: new Date().toISOString()
});

fs.writeFileSync(queueFile, JSON.stringify(queue, null, 2));
console.log(`[FILA] Mensagem de "${remetente}" para ${numero} enfileirada.`);
