// spec: Salesforce CRM Test Scenarios - FIXED
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Account Management Tests', () => {
  test('Create New Account with Complete Information', async ({ page }) => {
    // Navigate to Accounts module using the working pattern
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    await page.waitForSelector('h1:has-text("Home")', { timeout: 10000 });
    
    // Click on Accounts link in Global navigation (avoiding strict mode violation)
    await page.getByTitle('Accounts').click();
    await page.waitForURL(/.*lightning.*Account.*(list|home)/);
    
    // 1. From Accounts list view, click "New" button
    await page.getByRole('button', { name: 'New' }).click();
    
    // 2. Verify "New Account" dialog opens
    await expect(page.getByRole('heading', { name: 'New Account' })).toBeVisible();
    
    // 3. Fill in required field: Account Name with unique value
    const timestamp = Date.now();
    const accountName = `GlobalTech Solutions ${timestamp}`;
    await page.getByRole('textbox', { name: 'Account Name' }).fill(accountName);
    
    // 4. Fill in basic optional fields
    await page.getByRole('textbox', { name: 'Website' }).fill('https://techsolutions.com');
    await page.getByRole('textbox', { name: 'Phone' }).fill('+1-555-123-4567');
    
    // Select Type = "Customer" from dropdown
    await page.getByRole('combobox', { name: 'Type' }).click();
    await page.getByRole('option', { name: 'Customer' }).click();
    
    // 5. Save the account
    await page.getByRole('button', { name: 'Save', exact: true }).click();
    
    // 6. Verify account creation was successful
    // Wait for navigation to account detail page or success message
    await expect(page).toHaveURL(/.*lightning.*Account.*view/, { timeout: 10000 });
    
    // Verify we're on the account detail page with the correct account name
    await expect(page.getByRole('heading', { name: new RegExp(`Account.*${accountName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`) })).toBeVisible();
    
    // Verify key information is displayed (using more specific locators to avoid strict mode violations)
    await expect(page.getByText('Customer', { exact: true })).toBeVisible();
    await expect(page.getByRole('link', { name: 'https://techsolutions.com' })).toBeVisible();
    await expect(page.getByRole('link', { name: '+1-555-123-4567' })).toBeVisible();
    
    // Verify success message
    await expect(page.getByText('was created')).toBeVisible();
  });
});