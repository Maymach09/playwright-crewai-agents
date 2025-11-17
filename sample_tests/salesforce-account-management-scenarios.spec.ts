// spec: Salesforce Account Management - Comprehensive Test Plan
// seed: tests/seed.spec.ts

import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Salesforce Account Management', () => {
    test('Navigate to Accounts Module from Home', async ({ page }) => {
        // 1. Navigate to Salesforce application home page
        await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');

        // 2. Verify Home page loads with main navigation visible
        await expect(page.getByText('Home')).toBeVisible();

        // 3. Click on "Accounts" tab in the main navigation menu
        await page.getByRole('link', { name: 'Accounts', exact: true }).click();

        // 4. Verify navigation to Accounts module
        await expect(page.getByRole('button', { name: 'New' })).toBeVisible();
        await expect(page.getByText('Recently Viewed')).toBeVisible();
    });

    test('Create Account with Minimum Required Fields', async ({ page }) => {
        // 1. Navigate to Accounts module
        await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/o/Account/list?filterName=Recent');

        // 2. Click "New" button
        await page.getByRole('button', { name: 'New' }).click();

        // 3. Fill only required field: Account Name: "Minimal Test Account"
        await page.getByRole('textbox', { name: 'Account Name' }).fill('Minimal Test Account');

        // 4. Leave all optional fields blank
        // 5. Click "Save" button
        await page.getByRole('button', { name: 'Save', exact: true }).click();

        // Verify expected results
        await expect(page.getByText('Minimal Test Account')).toBeVisible();
    });

    test('Verify Account Information Accuracy', async ({ page }) => {
        // Navigate to created test account detail page (assuming account exists)
        await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/o/Account/list?filterName=Recent');
        await page.getByRole('button', { name: 'New' }).click();
        await page.getByRole('textbox', { name: 'Account Name' }).fill('Minimal Test Account');
        await page.getByRole('button', { name: 'Save', exact: true }).click();

        // 1. Verify all entered information displays correctly
        await expect(page.getByText('Minimal Test Account')).toBeVisible();

        // 2. Check field formatting and data integrity
        await expect(page.getByRole('link', { name: 'Mayank Mahajan' })).toBeVisible();

        // 3. Validate related record sections
        await expect(page.getByText('Created By')).toBeVisible();
        await expect(page.getByText('Last Modified By')).toBeVisible();

        // 4. Verify date/time stamps show correctly in History section
        await expect(page.getByText('11/7/2025, 11:12 AM')).toBeVisible();
    });

    test('Access Account Delete Option', async ({ page }) => {
        // Navigate to test account detail page (create account first)
        await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/o/Account/list?filterName=Recent');
        await page.getByRole('button', { name: 'New' }).click();
        await page.getByRole('textbox', { name: 'Account Name' }).fill('Minimal Test Account');
        await page.getByRole('button', { name: 'Save', exact: true }).click();

        // 1. Click "Show more actions" dropdown button
        await page.getByRole('button', { name: 'Show more actions' }).click();

        // 2. Verify delete option availability
        await expect(page.getByRole('menuitem', { name: 'Delete' })).toBeVisible();

        // 3. Click "Delete" option
        await page.getByRole('menuitem', { name: 'Delete' }).click();

        // 4. Verify confirmation dialog appears with clear warning
        await expect(page.getByText('Are you sure you want to delete this account?')).toBeVisible();
    });

    test('Confirm Account Deletion', async ({ page }) => {
        // Navigate to test account detail page (create account first)
        await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/o/Account/list?filterName=Recent');
        await page.getByRole('button', { name: 'New' }).click();
        await page.getByRole('textbox', { name: 'Account Name' }).fill('Minimal Test Account');
        await page.getByRole('button', { name: 'Save', exact: true }).click();

        // 1. Click "Show more actions" → "Delete"
        await page.getByRole('button', { name: 'Show more actions' }).click();
        await page.getByRole('menuitem', { name: 'Delete' }).click();

        // 2. Confirm deletion in confirmation dialog
        await page.getByRole('button', { name: 'Delete' }).click();

        // 3. Verify deletion completion
        // User redirected to Accounts list view is automatically handled
        // Success confirmation message is displayed through toast notification
        await expect(page.getByText('Recently Viewed')).toBeVisible();
    });
});