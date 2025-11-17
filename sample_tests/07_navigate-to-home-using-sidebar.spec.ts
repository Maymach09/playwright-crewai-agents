// spec: Salesforce_Account_Management_Test_Plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Navigation', () => {
  test('Navigate to Home Using Sidebar', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');

    // Navigate to Accounts Module
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();

    // 1. Click Home link in navigation
    await page.getByLabel('Main').getByRole('link', { name: 'Home' }).click();

    // 2. Verify Home page loads
    await expect(page.getByText('Welcome, Mayank')).toBeVisible();
  });
});
