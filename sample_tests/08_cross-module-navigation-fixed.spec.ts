// spec: Salesforce CRM Test Scenarios - FIXED
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Cross-Module Navigation Tests', () => {
  test('Cross-Module Navigation Flow', async ({ page }) => {
    // Start from the Salesforce home page
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    await new Promise(f => setTimeout(f, 3 * 1000));
    
    // 1. Navigate from Home to Accounts module
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    
    // Verify successful navigation to Accounts
    await expect(page.getByRole('heading', { name: 'Accounts', exact: true }).first()).toBeVisible();
    expect(page.url()).toContain('/lightning/o/Account/');
    
    // 2. Navigate from Accounts to Leads module (via Sales)
    await page.getByRole('link', { name: 'Sales', exact: true }).click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    
    // Verify successful navigation to Sales (which shows Leads)
    await expect(page.getByRole('heading', { name: 'Leads', exact: true }).first()).toBeVisible();
    expect(page.url()).toContain('/lightning/o/Lead/');
    
    // 3. Navigate back to Accounts from Sales
    await page.getByRole('link', { name: 'Accounts', exact: true }).first().click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    
    // Verify we're back in Accounts
    await expect(page.getByRole('heading', { name: 'Accounts', exact: true }).first()).toBeVisible();
    expect(page.url()).toContain('/lightning/o/Account/');
    
    // 4. Navigate to Contacts module
    await page.getByRole('link', { name: 'Contacts', exact: true }).first().click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    
    // Verify we're in Contacts
    await expect(page.getByRole('heading', { name: 'Contacts', exact: true }).first()).toBeVisible();
    expect(page.url()).toContain('/lightning/o/Contact/');
    
    // 5. Navigate back to Home from Contacts
    await page.getByLabel('Main').getByRole('link', { name: 'Home' }).click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    
    // Verify we're back on home page
    expect(page.url()).toContain('/lightning/page/home');
    
    // 6. Test direct navigation to Sales module
    await page.getByLabel('Main').getByRole('link', { name: 'Sales' }).click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    
    // Verify we're in a sales-related area (could be Leads page)
    const currentUrl = page.url();
    const isInSalesArea = currentUrl.includes('/lightning/o/Lead/') || 
                         currentUrl.includes('/lightning/app/') ||
                         currentUrl.includes('/sales');
    expect(isInSalesArea).toBeTruthy();
    
    // Go back to Home to complete the test
    await page.getByLabel('Main').getByRole('link', { name: 'Home' }).click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    expect(page.url()).toContain('/lightning/page/home');
    
    // 7. Verify all navigation links remain functional throughout the test
    // Final verification that key navigation elements are still present and working
    await expect(page.getByLabel('Main').getByRole('link', { name: 'Home' })).toBeVisible();
    await expect(page.getByLabel('Main').getByRole('link', { name: 'Accounts' })).toBeVisible();
    await expect(page.getByLabel('Main').getByRole('link', { name: 'Sales' })).toBeVisible();
    await expect(page.getByLabel('Main').getByRole('link', { name: 'Contacts' })).toBeVisible();
  });
});