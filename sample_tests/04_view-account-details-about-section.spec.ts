// spec: Salesforce_Account_Management_Test_Plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Account Operations', () => {
  test('View Account Details - About Section', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');

    // Navigate to Accounts Module
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();

    // Open Ledges Account
    await page.getByRole('link', { name: 'Ledges' }).click();

    // 1. Verify About section with Type field is visible
    await expect(page.getByRole('heading', { name: 'About' })).toBeVisible();
    await expect(page.getByText('Customer')).toBeVisible();
  });
});
