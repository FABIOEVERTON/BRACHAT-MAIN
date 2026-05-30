// send_aisio.js - Envia mensagem para Aisio via WhatsApp Business Web
const puppeteer = require('puppeteer');
const path = require('path');
const os = require('os');

const WA_PROFILE = path.join(os.homedir(), '.hermes-wa-session');
const PHONE = '5561991163206'; // Aisio

(async () => {
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: false,
      userDataDir: WA_PROFILE,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--window-size=1280,800',
      ],
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    console.log('Abrindo conversa com Aisio diretamente pelo numero...');

    // Open chat directly by phone number
    await page.goto(`https://web.whatsapp.com/send?phone=${PHONE}`, { waitUntil: 'domcontentloaded', timeout: 30000 });

    // Wait for the message box to appear
    console.log('Aguardando caixa de mensagem...');
    await page.waitForSelector(
      'div[contenteditable="true"][data-tab="10"], footer div[contenteditable="true"]',
      { timeout: 60000 }
    );

    const msgBox = await page.$('div[contenteditable="true"][data-tab="10"]') ||
                   await page.$('footer div[contenteditable="true"]');

    if (!msgBox) {
      console.error('Caixa de mensagem nao encontrada.');
      await page.screenshot({ path: os.homedir() + '/Desktop/wa_error.png' });
      await browser.close();
      process.exit(1);
    }

    console.log('Digitando mensagem...');
    const lines = [
      'Boa tarde Sr. Aisio. Meu nome e Gilmario. O Fabio acabou de me criar. Eu que a partir de agora estou cuidando da edicao do teu livro. O Fabio perguntou se podemos encontrar no domingo.',
      '',
      'bom te conhecer. Precisando de algo pode falar neste whatsapp.',
    ];

    await msgBox.click();
    for (let i = 0; i < lines.length; i++) {
      await msgBox.type(lines[i]);
      if (i < lines.length - 1) {
        await page.keyboard.down('Shift');
        await page.keyboard.press('Enter');
        await page.keyboard.up('Shift');
      }
    }

    console.log('Enviando...');
    await page.keyboard.press('Enter');
    await new Promise(r => setTimeout(r, 4000));

    await page.screenshot({ path: os.homedir() + '/Desktop/wa_sent.png' });
    console.log('MENSAGEM ENVIADA COM SUCESSO! Screenshot: ~/Desktop/wa_sent.png');

    await browser.close();
  } catch (err) {
    console.error('Erro:', err.message || err);
    if (browser) {
      try {
        const pages = await browser.pages();
        if (pages.length) await pages[0].screenshot({ path: os.homedir() + '/Desktop/wa_error.png' });
      } catch {}
    }
    process.exit(1);
  }
})();
