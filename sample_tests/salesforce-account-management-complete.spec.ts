// spec: Salesforce_Account_Management_Test_Plan.md
// Combined test script for all Salesforce Account Management scenarios

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Salesforce Account Management - Complete Flow', () => {
  
  test('Complete Account Management Flow', async ({ page }) => {
    // Navigate to Salesforce application using stored authentication state
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');

    // === SCENARIO 2.1: Navigate to Accounts Module ===
    // 1. From Salesforce Home page, click on "Accounts" link in navigation menu
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();

    // 2. Verify Accounts list view loads with "Recently Viewed" filter
    await expect(page.getByRole('heading', { name: 'Accounts' })).toBeVisible();

    // === SCENARIO 2.2: View Recently Viewed Accounts List ===
    // 1. Verify the accounts list displays recently accessed accounts
    // 2. Check item count is displayed
    await expect(page.getByText('1 item •')).toBeVisible();

    // === SCENARIO 3.1: Open Ledges Account ===
    // 1. Click on "Ledges" account link
    await page.getByRole('link', { name: 'Ledges' }).click();

    // 2. Verify account detail page loads
    await expect(page.getByRole('heading', { name: 'Account Ledges' })).toBeVisible();

    // === SCENARIO 3.2: View Account Details - About Section ===
    // 1. Verify About section with Type field is visible
    await expect(page.getByRole('heading', { name: 'About' })).toBeVisible();
    // Verify Type field exists (value may vary: Customer, Prospect, etc.)
    await expect(page.locator('span', { hasText: 'Type' }).first()).toBeVisible();

    // === SCENARIO 3.3: Edit Account Type Field - View Available Options ===
    // 1. Click "Edit Type" button
    await page.getByRole('button', { name: 'Edit Type' }).click();

    // 2. Click Type dropdown
    await page.getByRole('combobox', { name: 'Type' }).click();

    // 3. Verify all Type options are available
    await expect(page.getByRole('option', { name: 'Customer' })).toBeVisible();

    // === SCENARIO 3.4: Change Account Type and Save ===
    // 1. Select "Analyst" from Type dropdown
    await page.getByRole('option', { name: 'Prospect' }).click();

    // 2. Click Save
    await page.getByRole('button', { name: 'Save' }).click();

    // 3. Verify updated Type value using more specific locator
    await expect(page.locator('lightning-formatted-text').filter({ hasText: 'Prospect' }).first()).toBeVisible();

    // Change back to Customer for data consistency
    await page.getByRole('button', { name: 'Edit Type' }).click();
    await page.getByRole('combobox', { name: 'Type' }).click();
    await page.getByRole('option', { name: 'Customer' }).click();
    await page.getByRole('button', { name: 'Save' }).click();
    
    // Wait for save to complete and page to return to view mode
    await page.waitForTimeout(2000);

    // === SCENARIO 4.1: Navigate to Home Using Sidebar ===
    // 1. Click Home link in navigation
    await page.getByLabel('Main').getByRole('link', { name: 'Home' }).click();

    // 2. Verify Home page loads
    await expect(page.getByRole('heading', { name: 'Welcome, Mayank' })).toBeVisible();
  });
});
