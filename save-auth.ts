// save-auth.ts
import { chromium } from 'playwright';
import * as fs from 'fs';

(async () => {
  console.log('🚀 Launching browser...');
  const browser = await chromium.launch({ headless: false }); // run in headed mode
  const context = await browser.newContext();
  const page = await context.newPage();

  console.log('🌐 Navigating to Salesforce login page...');
  await page.goto('https://login.salesforce.com');

  console.log(`
  ✅ Please log in manually and complete 2FA.
  👉 Once you see your Salesforce home page, return to this terminal and press ENTER.
  `);

  // Wait for user to press Enter
  await new Promise<void>((resolve) => {
    process.stdin.resume();
    process.stdin.once('data', () => {
      process.stdin.pause();
      resolve();
    });
  });

  const path = 'auth_state.json';
  await context.storageState({ path });
  console.log(`✅ Saved authentication state to ${path}`);

  await browser.close();
  process.exit(0);
})();