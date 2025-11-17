// spec: test_plan/salesforce_test_plan.md 
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Salesforce Lightning Experience - Navigation and Data Verification Tests', () => {
  test('Navigate to Accounts and verify "Ledges" account is available', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');
    
    // 1. Click the "Accounts" tab in Main navigation.
    await page.click('role=link[name="Accounts"]');
    
    // 2. Wait for the Accounts list view page to load (Recently Viewed by default).
    await page.waitForSelector('text=Recently Viewed', { timeout: 10000 });
    
    // 3. Observe the list table and scan for a row with “Ledges”.
    const isLedgesVisible = await page.isVisible('role=link[name="Ledges"]');
    
    // 4. Verify the link “Ledges” is visible in the Account Name column.
    expect(isLedgesVisible).toBe(true);
    
    // Expected Results:
    // - Accounts page heading is visible.
    // - The “Ledges” link appears in the list grid.
    // - No errors in navigation or loading.
  });
});
