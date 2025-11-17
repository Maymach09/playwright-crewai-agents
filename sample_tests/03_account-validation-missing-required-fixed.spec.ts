// spec: Salesforce CRM Test Scenarios - FIXED
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Account Management Tests', () => {
  test('Account Creation Validation - Missing Required Field', async ({ page }) => {
    // Navigate to Accounts module
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    await new Promise(f => setTimeout(f, 5 * 1000));
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();
    
    // 1. Navigate to Accounts list view
    await expect(page.getByRole('heading', { name: 'Accounts' })).toBeVisible();
    
    // 2. Click "New" button
    await page.getByRole('button', { name: 'New' }).first().click();
    await expect(page.getByRole('heading', { name: 'New Account' })).toBeVisible();
    
    // 3. Leave Account Name field empty (required field)
    // 4. Fill optional fields (Website, Phone)
    await page.getByRole('textbox', { name: 'Website' }).fill('https://example.com');
    await page.getByRole('textbox', { name: 'Phone' }).fill('+1-555-000-0000');
    
    // 5. Attempt to click "Save" button
    await page.getByRole('button', { name: 'Save', exact: true }).click();
    
    // Verify save operation fails and dialog remains open (URL should still contain 'new')
    expect(page.url()).toContain('/new');
    await expect(page.getByRole('heading', { name: 'New Account' })).toBeVisible();
    
    // Verify form remains open with entered data preserved
    await expect(page.getByRole('textbox', { name: 'Website' })).toHaveValue('https://example.com');
    await expect(page.getByRole('textbox', { name: 'Phone' })).toHaveValue('+1-555-000-0000');
    
    // Verify Account Name field is still empty
    await expect(page.getByRole('textbox', { name: 'Account Name' })).toHaveValue('');
    
    // User can correct the error and retry
    const timestamp = Date.now();
    await page.getByRole('textbox', { name: 'Account Name' }).fill(`Test Account ${timestamp}`);
    await page.getByRole('button', { name: 'Save', exact: true }).click();
    
    // Handle any potential duplicate dialogs
    try {
      const closeButton = page.getByRole('button', { name: 'Close error dialog' });
      if (await closeButton.isVisible({ timeout: 2000 })) {
        await closeButton.click();
        // Try with different name if duplicate detected
        await page.getByRole('textbox', { name: 'Account Name' }).fill(`Unique Test Account ${timestamp}-${Math.random().toString(36).substring(7)}`);
        await page.getByRole('button', { name: 'Save', exact: true }).click();
      }
    } catch (error) {
      // No dialog appeared
    }
    
    // Verify successful creation after fixing the error
    // Check that we're no longer on the 'new' page, indicating successful save
    await new Promise(f => setTimeout(f, 3 * 1000));
    const currentUrl = page.url();
    const isAccountCreated = currentUrl.includes('/lightning/r/Account/') || 
                           !currentUrl.includes('/new');
    expect(isAccountCreated).toBeTruthy();
  });
});