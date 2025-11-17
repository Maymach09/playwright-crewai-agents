// spec: Salesforce_Navigation_Test_Plan.md
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Salesforce Lightning Experience - Navigation and Data Verification Tests', () => {
  
  test('Navigate to Accounts Tab and Verify Ledges Account', async ({ page }) => {
    // Start from the Home page of the Salesforce Lightning Experience
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');
    await page.locator('li').filter({ hasText: 'Home' }).click();
    
    // Click on the "Accounts" tab in the main navigation menu
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();
    
    // Wait for the Accounts page to load completely
    // Verify that the page title shows "Recently Viewed | Accounts | Salesforce"
    await expect(page).toHaveTitle(/Recently Viewed \| Accounts \| Salesforce/);
    
    // Verify that the page URL contains "/lightning/o/Account/list?filterName=Recent"
    await expect(page).toHaveURL(/.*\/lightning\/o\/Account\/list\?filterName=Recent/);
    
    // Locate the accounts data grid/table and verify that "Ledges" account is visible
    await expect(page.getByRole('link', { name: 'Ledges' })).toBeVisible();
  });

  test('Navigate to Sales Tab and Verify Robert Anderson Lead', async ({ page }) => {
    // Navigate to the application
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');
    await page.locator('li').filter({ hasText: 'Home' }).click();
    
    // Click on the "Sales" tab in the main navigation
    await page.getByRole('link', { name: 'Sales', exact: true }).first().click();
    
    // Wait for the Sales page to load completely
    await page.getByText("Robert Anderson").first().waitFor({ state: 'visible' });
    
    // Verify that the page navigates to the Leads section by default
    // Verify that the page title shows "Recently Viewed | Leads | Salesforce"
    await expect(page).toHaveTitle(/Recently Viewed \| Leads \| Salesforce/);
    
    // Verify that the page URL contains "/lightning/o/Lead/list?filterName=Recent"
    await expect(page).toHaveURL(/.*\/lightning\/o\/Lead\/list\?filterName=Recent/);
    
    // Locate the leads data grid/table and verify that "Robert Anderson" lead is visible
    await expect(page.getByRole('link', { name: 'Robert Anderson' })).toBeVisible();
  });

  test('Verify Sales Module Navigation Options', async ({ page }) => {
    // Navigate to the Sales page
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');
    await page.locator('li').filter({ hasText: 'Home' }).click();
    await page.getByRole('link', { name: 'Sales', exact: true }).first().click();
    
    // Wait for page to load
    await page.getByText("Robert Anderson").first().waitFor({ state: 'visible' });
    
    // Verify that the left navigation shows all available sales modules
    // Check that the following options are available: Leads, Contacts, Accounts, Opportunities, Products, Price Books, Calendar, Analytics
    const salesNavigation = page.getByRole('navigation', { name: 'Global' });
    await expect(salesNavigation.getByRole('link', { name: 'Leads' })).toBeVisible();
    await expect(salesNavigation.getByRole('link', { name: 'Contacts' })).toBeVisible();
    await expect(salesNavigation.getByRole('link', { name: 'Accounts' })).toBeVisible();
    await expect(salesNavigation.getByRole('link', { name: 'Opportunities' })).toBeVisible();
    await expect(salesNavigation.getByRole('link', { name: 'Products' })).toBeVisible();
    await expect(salesNavigation.getByRole('link', { name: 'Price Books' })).toBeVisible();
    await expect(salesNavigation.getByRole('link', { name: 'Calendar' })).toBeVisible();
    await expect(salesNavigation.getByRole('link', { name: 'Analytics' })).toBeVisible();
    
    // Verify that action buttons are available: New, Import, Add to Campaign, Send Email, Change Owner
    await expect(page.getByRole('button', { name: 'New' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Import' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Add to Campaign' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Send Email' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Change Owner' })).toBeVisible();
  });

  test('Navigate to Home Page and Verify Dashboard Elements', async ({ page }) => {
    // Navigate to the application
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');
    await page.locator('li').filter({ hasText: 'Home' }).click();
    
    // Click on the "Home" tab in the main navigation
    await page.getByLabel('Main').getByRole('link', { name: 'Home' }).click();
    
    // Wait for the Home page to load completely
    // Verify that the page title shows "Home | Salesforce"
    await expect(page).toHaveTitle(/Home \| Salesforce/);
    
    // Verify that the page URL contains "/lightning/page/home"
    await expect(page).toHaveURL(/.*\/lightning\/page\/home/);
    
    // Verify that the welcome message shows "Welcome, Mayank"
    await expect(page.getByRole('heading', { name: 'Welcome, Mayank' })).toBeVisible();
    
    // Check that suggestion cards are displayed
    await expect(page.getByText('Create your first contact').first()).toBeVisible();
    await expect(page.getByText('Turn on marketing features').first()).toBeVisible();
    await expect(page.getByText('Visualize your data with AI').first()).toBeVisible();
    
    // Verify that dashboard reports are visible
    await expect(page.getByRole('heading', { name: 'Recent Records' })).toBeVisible();
    
    // Verify Recent Records section displays recent activity including "Ledges" account and "Robert Anderson" lead
    await expect(page.getByRole('link', { name: 'Ledges' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Robert Anderson' })).toBeVisible();
  });

  test('Verify Application State Persistence', async ({ page }) => {
    // Navigate to the application starting point
    await page.goto('https://nosoftware-saas-2365.my.salesforce.com/');
    await page.locator('li').filter({ hasText: 'Home' }).click();
    
    // Navigate through different tabs (Home → Accounts → Sales → Home)
    // Verify each navigation maintains proper application state
    
    // Step 1: Verify Home page state
    await page.getByLabel('Main').getByRole('link', { name: 'Home' }).click();
    await expect(page).toHaveURL(/.*\/lightning\/page\/home/);
    await expect(page.getByRole('heading', { name: 'Welcome, Mayank' })).toBeVisible();
    
    // Step 2: Navigate to Accounts and verify state persistence
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();
    await expect(page).toHaveURL(/.*\/lightning\/o\/Account\/list\?filterName=Recent/);
    await expect(page).toHaveTitle(/Recently Viewed \| Accounts \| Salesforce/);
    await expect(page.getByRole('link', { name: 'Ledges' })).toBeVisible();
    
    // Step 3: Navigate to Sales and verify state persistence
    await page.getByRole('link', { name: 'Sales' }).click();
    await expect(page).toHaveURL(/.*\/lightning\/o\/Lead\/list\?filterName=Recent/);
    await expect(page).toHaveTitle(/Recently Viewed \| Leads \| Salesforce/);
    await expect(page.getByRole('link', { name: 'Robert Anderson' })).toBeVisible();
    
    // Step 4: Return to Home and verify state persistence
    await page.getByLabel('Main').getByRole('link', { name: 'Home' }).click();
    await expect(page).toHaveURL(/.*\/lightning\/page\/home/);
    await expect(page).toHaveTitle(/Home \| Salesforce/);
    await expect(page.getByRole('heading', { name: 'Welcome, Mayank' })).toBeVisible();
    
    // Verify that recently viewed items update appropriately
    await expect(page.getByRole('link', { name: 'Ledges' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Robert Anderson' })).toBeVisible();
    
    // Verify that user session remains active throughout navigation
    await expect(page.getByRole('button', { name: 'View profile' })).toBeVisible();
  });
});