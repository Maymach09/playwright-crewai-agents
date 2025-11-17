// spec: Salesforce_Account_Management_Test_Plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Account Operations', () => {
  test('Change Account Type and Save', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');

    // Navigate to Accounts Module
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();

    // Open Ledges Account
    await page.getByRole('link', { name: 'Ledges' }).click();

    // Click Edit Type button
    await page.getByRole('button', { name: 'Edit Type' }).click();

    // 1. Select "Customer" from Type dropdown
    await page.getByRole('combobox', { name: 'Type' }).click();
    await page.getByRole('option', { name: 'Customer' }).click();

    // 2. Click Save
    await page.getByRole('button', { name: 'Save' }).click();

    // 3. Verify success message and updated Type value
    await expect(page.getByText('Customer')).toBeVisible();
  });
});
