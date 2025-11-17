import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Create Account', () => {
  test('Happy Path - Create Account with Minimum Required Data', async ({ page }) => {
    // 1. Navigate to the Salesforce Accounts module.
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();
    await expect(page).toHaveURL(/.*Account.*/);
    await expect(page).toHaveTitle(/Recently Viewed | Accounts | Salesforce/);

    // 2. Click on the "New" button to create a new account.
    await page.getByRole('button', { name: 'New' }).click();
    await expect(page).toHaveTitle(/New Account/);

    // 3. Fill in the "Account Name" field.
    await page.getByRole('textbox', { name: 'Account Name', exact: true }).fill('Test Account 2');
    await expect(page.getByRole('textbox', { name: 'Account Name', exact: true })).toHaveValue('Test Account 2');

    // 4. Click on the "Save" button to save the new account.
    await page.getByRole('button', { name: 'Save', exact: true }).click();
    await expect(page).toHaveURL(/.*Account/);
    await expect(page.getByText('Test Account 2')).toBeVisible();
  });
});