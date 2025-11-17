import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Start Salesforce Application', () => {
  test('Navigate to Homes Page', async ({ page }) => {
    // 1. Open Salesforce application (starting from Home page)
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    //await new Promise(f => setTimeout(f, 5 * 1000));
    console.log('✅ Salesforce home page loaded successfully');
  });
});