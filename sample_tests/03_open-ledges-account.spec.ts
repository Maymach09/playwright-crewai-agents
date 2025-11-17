// spec: Salesforce_Account_Management_Test_Plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Account Operations', () => {
  test('Open Ledges Account', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');

    // Navigate to Accounts Module
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();

    // 1. Click on "Ledges" account link
    await page.getByRole('link', { name: 'Ledges' }).click();

    // 2. Verify account detail page loads
    await expect(page.getByRole('heading', { name: 'Account Ledges' })).toBeVisible();
  });
});
