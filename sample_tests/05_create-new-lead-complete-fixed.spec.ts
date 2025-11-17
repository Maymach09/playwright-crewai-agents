// spec: Salesforce CRM Test Scenarios - FIXED
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Lead Management Tests', () => {
  test('Create New Lead with Complete Information', async ({ page }) => {
    // Set longer timeout for this test
    test.setTimeout(60000);
    
    // Navigate to Leads section
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    await page.waitForTimeout(3000);
    
    // 1. Navigate to Leads section via Sales app
    await page.getByRole('link', { name: 'Sales', exact: true }).click();
    await page.waitForTimeout(2000);
    
    // Verify we're in the Sales section
    await expect(page.getByRole('heading', { name: 'Sales', exact: true })).toBeVisible();
    
    // Navigate to Leads
    await page.getByRole('link', { name: 'Leads', exact: true }).click();
    await page.waitForTimeout(2000);
    
    // Verify we're in the Leads list view
    await expect(page.getByRole('heading', { name: 'Leads', exact: true })).toBeVisible();
    
    // 2. From Leads list view, click "New" button
    await page.getByRole('button', { name: 'New' }).first().click();
    await page.waitForTimeout(2000);
    await expect(page.getByRole('heading', { name: 'New Lead' })).toBeVisible();
    
    // 3. Fill required fields for the lead
    const timestamp = Date.now();
    console.log(`Using timestamp: ${timestamp}`);
    
    // Fill First Name and Last Name (required)
    await page.getByRole('textbox', { name: 'First Name' }).fill('Robert');
    await page.getByRole('textbox', { name: 'Last Name' }).fill(`TestLead-${timestamp}`);
    
    // Fill Company (required)
    await page.getByRole('textbox', { name: 'Company' }).fill(`Test Company ${timestamp}`);
    
    // Fill optional fields
    await page.getByRole('textbox', { name: 'Title' }).fill('Test Manager');
    await page.getByRole('textbox', { name: 'Email' }).fill(`test${timestamp}@example.com`);
    await page.getByRole('textbox', { name: 'Phone' }).fill('+1-555-000-1234');
    
    // Wait for form to be fully loaded
    await page.waitForTimeout(1000);
    
    // 4. Handle potential duplicate dialog first (if it appears before save)
    try {
      const duplicateDialog = page.getByRole('dialog', { name: 'Similar Records Exist' });
      if (await duplicateDialog.isVisible({ timeout: 2000 })) {
        console.log('Pre-save duplicate dialog detected - closing...');
        await page.getByRole('button', { name: 'Close error dialog' }).click();
        await page.waitForTimeout(1000);
      }
    } catch (error) {
      console.log('No pre-save duplicate dialog found');
    }
    
    // Save the lead using multiple selector strategies
    console.log('Attempting to save lead...');
    const saveSelectors = [
      'button[name="SaveEdit"]',
      'button:has-text("Save"):not(:has-text("Save & New"))',
      'button[type="button"]:has-text("Save"):not(:has-text("&"))'
    ];
    
    let saveClicked = false;
    for (const selector of saveSelectors) {
      try {
        const saveButton = page.locator(selector);
        if (await saveButton.isVisible({ timeout: 2000 })) {
          await saveButton.click();
          console.log(`✅ Successfully clicked save button with selector: ${selector}`);
          saveClicked = true;
          break;
        }
      } catch (error) {
        console.log(`❌ Failed to click save with selector: ${selector}`);
        continue;
      }
    }
    
    if (!saveClicked) {
      // Fallback to role-based selector with exact match
      try {
        await page.getByRole('button', { name: 'Save', exact: true }).click();
        console.log('✅ Used fallback role-based save button');
      } catch (error) {
        console.log('❌ All save button attempts failed');
        throw error;
      }
    }
    
    // Wait for save operation
    await page.waitForTimeout(3000);
    
    // Handle potential duplicate dialog after save attempt
    try {
      const duplicateDialog = page.getByRole('dialog', { name: 'Similar Records Exist' });
      if (await duplicateDialog.isVisible({ timeout: 3000 })) {
        console.log('Post-save duplicate dialog detected - closing...');
        await page.getByRole('button', { name: 'Close error dialog' }).click();
        await page.waitForTimeout(1000);
        
        // Try saving again after closing duplicate dialog using alternative selector
        console.log('Attempting to save lead again after closing duplicate dialog...');
        try {
          await page.locator('button[name="SaveEdit"]').click();
          console.log('✅ Used SaveEdit button on retry');
        } catch (error) {
          await page.getByRole('button', { name: 'Save', exact: true }).click();
          console.log('✅ Used role-based save button on retry');
        }
        await page.waitForTimeout(3000);
      }
    } catch (error) {
      console.log('No post-save duplicate dialog found');
    }
    
    // 5. Verify successful lead creation
    console.log('Verifying lead creation...');
    
    // Check for success indicators
    const currentUrl = page.url();
    console.log(`Current URL: ${currentUrl}`);
    
    // Multiple ways to verify success
    const successChecks = [
      // Check if we navigated to lead detail page
      () => currentUrl.includes('/lightning/r/Lead/'),
      // Check if success notification is visible
      async () => {
        try {
          return await page.getByText(/was created/).isVisible({ timeout: 2000 });
        } catch {
          return false;
        }
      },
      // Check if we're no longer on the new page
      () => !currentUrl.includes('/new'),
      // Check if we can see the lead in the list
      async () => {
        try {
          return await page.getByText(`TestLead-${timestamp}`).isVisible({ timeout: 2000 });
        } catch {
          return false;
        }
      }
    ];
    
    let isSuccess = false;
    for (const check of successChecks) {
      const result = typeof check === 'function' ? await check() : check;
      if (result) {
        isSuccess = true;
        console.log('✅ Lead creation verified');
        break;
      }
    }
    
    // Final assertion
    expect(isSuccess).toBeTruthy();
    console.log('✅ Lead created successfully');
  });
});