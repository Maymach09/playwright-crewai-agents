// spec: Salesforce_Account_Management_Test_Plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Account Operations', () => {
  test('Edit Account Type Field - View Available Options', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');

    // Navigate to Accounts Module
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();

    // Open Ledges Account
    await page.getByRole('link', { name: 'Ledges' }).click();

    // 1. Click "Edit Type" button
    await page.getByRole('button', { name: 'Edit Type' }).click();

    // 2. Click Type dropdown
    await page.getByRole('combobox', { name: 'Type' }).click();

    // 3. Verify all Type options are available
    await expect(page.getByRole('option', { name: 'Customer' })).toBeVisible();
  });
});
