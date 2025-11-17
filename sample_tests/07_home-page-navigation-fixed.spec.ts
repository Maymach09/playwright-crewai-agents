// spec: Salesforce CRM Test Scenarios - FIXED
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Navigation Tests', () => {
  test('Home Page Navigation and Key Elements Validation', async ({ page }) => {
    // 1. Navigate directly to the Salesforce home page
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    await new Promise(f => setTimeout(f, 3 * 1000));
    
    // Verify successful navigation to home page
    expect(page.url()).toContain('/lightning/page/home');
    
        // 2. Verify key navigation elements are present and visible
    // Check that we have a main navigation area
    await expect(page.getByRole('navigation', { name: 'Main' })).toBeVisible();
    
    // Verify primary navigation links using more specific selectors
    await expect(page.getByLabel('Main').getByRole('link', { name: 'Home' })).toBeVisible();
    await expect(page.getByLabel('Main').getByRole('link', { name: 'Accounts' })).toBeVisible();
    await expect(page.getByLabel('Main').getByRole('link', { name: 'Sales' })).toBeVisible();
    
    // 3. Verify Home page specific elements
    // Check for welcome message or home content
    await expect(page.getByRole('heading', { name: 'Welcome, Mayank' })).toBeVisible();
    
    // Verify the main home content area is present
    await expect(page.getByRole('main')).toBeVisible();
    
    // Check for user profile/settings access
    await expect(page.getByRole('button', { name: 'View profile' })).toBeVisible();
    
    // 4. Verify key functional elements are present
    // Check search functionality is available
    await expect(page.getByText('Search...')).toBeVisible();
    
    // Verify navigation to core modules works
    await page.getByLabel('Main').getByRole('link', { name: 'Accounts' }).click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    expect(page.url()).toContain('/Account/');
    
    // Navigate back to Home
    await page.getByLabel('Main').getByRole('link', { name: 'Home' }).click();
    await new Promise(f => setTimeout(f, 2 * 1000));
    expect(page.url()).toContain('/lightning/page/home');
  });
});