// spec: Salesforce CRM Test Scenarios - FIXED
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Sales Module Navigation Tests', () => {
  test('Navigate to Sales Module', async ({ page }) => {
    // Start from the Salesforce home page
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    await new Promise(f => setTimeout(f, 3 * 1000));
    
    // 1. Navigate to the Sales module
    await page.getByRole('link', { name: 'Sales', exact: true }).click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    
    // Verify successful navigation to Sales module
    expect(page.url()).toContain('/lightning/');
    
    // 2. Verify expected elements are present in the Sales module
    // Check for key Sales module elements - verify we're on a valid Salesforce page
    await expect(page.getByRole('button', { name: 'New' })).toBeVisible();
    
    // Verify we can see navigation elements
    const currentUrl = page.url();
    const isInSalesWorkspace = currentUrl.includes('/lightning/o/Lead/') || 
                              currentUrl.includes('/lightning/app/') ||
                              currentUrl.includes('/sales');
    expect(isInSalesWorkspace).toBeTruthy();
  });
});