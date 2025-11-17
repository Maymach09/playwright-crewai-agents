// spec: test_plan/salesforce_test_plan.md 
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Salesforce Lightning Experience - Navigation and Data Verification Tests', () => {
  test('Navigate to Accounts and verify "Robert Anderson" account is available', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');
    
    // 1. Click the “Sales” tab in Main navigation (Leads list loads by default).
    await page.click('role=link[name="Sales"]');
    
    // 2. Wait for the link to become visible instead of using a plain wait
    await page.waitForSelector('role=link[name="Robert Anderson"]'); 
    
    // 3. Observe the list grid and locate the “Robert Anderson” link in the Name column.
    const isRobertVisible = await page.isVisible('role=link[name="Robert Anderson"]');
    
    // 4. Verify the “Robert Anderson” link is visible.
    expect(isRobertVisible).toBe(true);
  });
});
