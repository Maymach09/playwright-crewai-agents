// spec: Salesforce CRM Test Scenarios - FIXED
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Account Management Tests', () => {
  test('Navigate to Accounts Module', async ({ page }) => {
    // 1. Open Salesforce application (starting from Home page)
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    await new Promise(f => setTimeout(f, 5 * 1000));
    
    // 2. Click on "Accounts" tab in the main navigation menu
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();
    
    // 3. Verify the Accounts list view loads
    await expect(page.getByRole('heading', { name: 'Accounts', exact: true })).toBeVisible();
    await expect(page.getByRole('button', { name: 'New' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Ledges' })).toBeVisible();
    
    // Verify URL changes to the correct accounts list view
    expect(page.url()).toContain('/lightning/o/Account/list?filterName=Recent');
  });
});