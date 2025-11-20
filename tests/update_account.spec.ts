import { test, expect } from '@playwright/test';

test.use({ storageState: 'auth_state.json' });

test.describe('Update Account Name and Phone Number', () => {
  test('Edit Account Details', async ({ page }) => {
    // 1. Navigate to the Salesforce Accounts module.
    await page.goto('https://nosoftware-saas-2365.lightning.force.com/lightning/page/home');

    // 2. Click on the 'Accounts' link in the navigation.
    await page.getByRole('link', { name: 'Accounts', exact: true }).click();

    // 3. Select the account 'Test Account 2' from the list.
    await page.getByRole('link', { name: 'Test Account 2' }).click();

    // 4. Click the 'Edit' button to modify account details.
    await page.getByRole('button', { name: 'Edit', exact: true }).click();

    // 5. Fill in the updated account name and phone number.
    await page.getByRole('textbox', { name: 'Account Name' }).fill('Updated Test Account 2');
    await page.getByRole('textbox', { name: 'Phone' }).fill('123-456-1234');

    // 6. Click the 'Save' button to update the account details.
    await page.getByRole('button', { name: 'Save', exact: true }).click();

    // 7. Verify the account name is updated.
    await expect(page.getByRole('link', { name: 'Updated Test Account 2', exact: true })).toBeVisible();

    // 8. Verify the phone number is updated.
    await expect(page.getByText('123-456-1234')).toBeVisible();
  });
});
