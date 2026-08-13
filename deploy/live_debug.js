const puppeteer = require('/tmp/tb_debug/node_modules/puppeteer-core');
const fs = require('fs');

async function main() {
    const serverUrl = process.env.TB_SERVER || 'http://10.25.7.152:8080';
    const widgetId = process.argv[2] || '129b14c0-961c-11f1-93f6-e901e04b0375';

    console.log(`=== AGENT LIVE DEBUGGER FOR WIDGET: ${widgetId} ===`);
    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/google-chrome',
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1600,1000']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1600, height: 1000 });

    const errors = [];
    page.on('console', msg => console.log(`[Console ${msg.type().toUpperCase()}] ${msg.text()}`));
    page.on('pageerror', err => {
        console.error('=== UNCAUGHT EXCEPTION ===', err.stack || err.toString());
        errors.push(err.toString());
    });

    try {
        await page.goto(`${serverUrl}/login`, { waitUntil: 'networkidle2' });
        await page.waitForSelector('input[type="email"], input[name="username"], input[formcontrolname="username"]');
        await page.type('input[type="email"], input[name="username"], input[formcontrolname="username"]', 'admin_assa@inergy.vn');
        await page.type('input[type="password"]', 'Amitech@123');
        await page.click('button[type="submit"]');
        await page.waitForNavigation({ waitUntil: 'networkidle2' });

        const targetUrl = `${serverUrl}/resources/widgets-library/widgets/${widgetId}`;
        console.log(`Navigating to Widget Editor: ${targetUrl}`);
        await page.goto(targetUrl, { waitUntil: 'networkidle2' });
        await new Promise(r => setTimeout(r, 4000));

        const screenshotPath = `/tmp/agent_widget_${widgetId}_debug.png`;
        await page.screenshot({ path: screenshotPath });
        console.log(`Saved live screenshot to: ${screenshotPath}`);

        if (errors.length === 0) {
            console.log('✅ PASSED! ZERO UNCAUGHT EXCEPTIONS DETECTED.');
        } else {
            console.error(`❌ FAILED! DETECTED ${errors.length} UNCAUGHT EXCEPTIONS.`);
        }
    } catch (e) {
        console.error('Error during live debug:', e);
    } finally {
        await browser.close();
    }
}

main();
