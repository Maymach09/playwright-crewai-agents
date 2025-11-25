import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Create New Account in Salesforce', () => {
  test('Create Account', async ({ page }) => {
    // 1. Navigate to the Accounts section.
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();

    // 2. Click on the New button to create a new account.
    await page.getByRole('button', { name: 'New', exact: true }).nth(0).click();

    // 3. Wait for the Account Name textbox to be visible before filling it.
    await page.waitForSelector('input[aria-label="Account Name"]', { timeout: 30000 });
    await page.getByRole('textbox', { name: 'Account Name' }).fill('Test Account 5');

    // 4. Fill in the Phone field.
    await page.getByRole('textbox', { name: 'Phone' }).fill('123-456-7890');

    // 5. Click on the Save button to save the new account.
    await page.getByRole('button', { name: 'Save', exact: true }).click();

    // Verify that the new account is visible in the Accounts list.
    await expect(page.getByText('Test Account')).toBeVisible();
  });
});
