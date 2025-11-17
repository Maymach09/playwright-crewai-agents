// spec: test_plan/salesforce_test_plan.md 
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Home Page Navigation', () => {
  test('Navigate to Home page and validate key elements', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');
    
    // 1. Click the "Home" tab in Main navigation (or click the Home icon/logo).
    await page.click('role=link[name="Home"]');
    
    // 2. Wait for the Home page to load by checking for specific elements.
    await page.waitForSelector('role=heading[name="Home"]', { timeout: 10000 });
    
    // 3. Verify the “Home” heading is visible.
    const isHomeHeadingVisible = await page.isVisible('role=heading[name="Home"]');
    
    // 4. Optionally validate “Recent Records” displays items.
    const isRecentRecordsVisible = await page.isVisible('text=Recent Records');
    
    // 5. Verify the results.
    expect(isHomeHeadingVisible).toBe(true);
    expect(isRecentRecordsVisible).toBe(true);
    
    // Expected Results:
    // - Home page renders with heading “Home”.
    // - “Recent Records” card shows recently viewed/available records.
  });
});
