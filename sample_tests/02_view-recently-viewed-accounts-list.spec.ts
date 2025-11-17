// spec: Salesforce_Account_Management_Test_Plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Accounts Module Navigation', () => {
  test('View Recently Viewed Accounts List', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');

    // Navigate to Accounts Module
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();

    // 1. Verify the accounts list displays recently accessed accounts
    // 2. Check item count is displayed
    await expect(page.getByText('1 item •')).toBeVisible();
  });
});
