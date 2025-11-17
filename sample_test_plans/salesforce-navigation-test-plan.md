# Salesforce Lightning (Home, Accounts, Sales/Leads) — Navigation and Data Presence Test Plan

## Executive Summary
This test plan validates key navigation paths and the presence of specific records in a Salesforce Lightning environment. The focus is to:
- Navigate to Accounts and verify the presence of an account named "Ledges".
- Navigate to Sales (Leads) and verify the presence of a lead named "Robert Anderson".
- Navigate to the Home page.
- Close the browser.

The plan includes happy paths, edge cases, validation steps, and clearly defined success/failure criteria. It is designed to be executed manually or automated (Playwright, Selenium, etc.) using robust, role-based selectors.

## Application Overview
The application under test is Salesforce Lightning, featuring a global navigation bar and object-specific list views. Key areas involved in this plan:
- Global navigation: Home, Contacts, Accounts, Sales, Service, Marketing, Commerce, etc.
- Accounts object: List views (e.g., Recently Viewed, All Accounts), record tables, and actions.
- Sales app: Defaults to Leads navigation with list views (e.g., Recently Viewed), grid table, and actions.
- Home page: Cards such as Recent Records and reporting widgets.

Observed environment pages (from exploration):
- Home: https://nosoftware-saas-2365.lightning.force.com/lightning/page/home
- Accounts (Recently Viewed list): https://nosoftware-saas-2365.lightning.force.com/lightning/o/Account/list?filterName=Recent
- Sales > Leads (Recently Viewed list): https://nosoftware-saas-2365.lightning.force.com/lightning/o/Lead/list?filterName=Recent

## Test Environment and Assumptions
- Environment URL: https://nosoftware-saas-2365.lightning.force.com/
- Browser: Chromium/Chrome (latest), screen size default desktop.
- Authentication: Valid Salesforce test user with permission to view Accounts and Leads.
- Starting State: Fresh browser session, user logged in and at the Home page, no cached list state required.
- Data Assumptions:
  - Account record named "Ledges" exists and is accessible to the test user.
  - Lead record named "Robert Anderson" exists and is accessible to the test user.
- Network: Stable connection; moderate latency may be present. List views may show Loading... states.

## Risks and Dependencies
- Data volatility: Target records may be renamed or deleted by parallel users.
- List view filters: "Recently Viewed" may not include target records; switching to wider list views or searching may be required.
- Permissions: User roles could restrict visibility to objects or records.
- Session/Timeouts: Login or session expiration can interrupt tests.

## Test Data
- Account: "Ledges"
- Lead: "Robert Anderson"
Note: This plan does not create or modify data. If data is missing, see Edge Cases for alternative verification steps.

## Execution Notes for Automation
- Prefer ARIA role and accessible name locators to increase test resilience:
  - Accounts tab: getByRole('link', { name: 'Accounts' })
  - Sales tab: getByRole('link', { name: 'Sales' })
  - Account link: getByRole('link', { name: 'Ledges' })
  - Lead link: getByRole('link', { name: 'Robert Anderson' })
- Wait strategy: Wait for transient loaders to disappear, e.g., wait for text "Loading..." to be hidden before asserting grid contents.

## Test Scenarios

### Scenario 1: Navigate to Accounts and verify the "Ledges" account exists
- Assumptions:
  - User is logged in and has access to Accounts.
  - An account named "Ledges" exists.
- Steps:
  1. Ensure the global navigation bar is visible with links including Accounts.
  2. Click the Accounts link in the global navigation.
  3. Wait for the Accounts list view to load (e.g., wait for any "Loading..." text to disappear and the grid to be visible).
  4. Observe the active list view (often "Recently Viewed"). If the target record is not visible:
     - Option A: Use the search within the list view to search for "Ledges".
     - Option B: Switch to a broader list view (e.g., "All Accounts"), then search for "Ledges" if needed.
  5. Verify the account link named "Ledges" is visible in the list grid.
  6. Optional: Click the "Ledges" link to open the record detail page and validate the record header shows "Ledges".
- Expected Results:
  - Accounts list page is displayed with the grid loaded.
  - A link named "Ledges" is present and visible in the table.
  - Optional: Record detail header reads "Ledges" when opened.
- Success Criteria:
  - The "Ledges" account link is displayed in the Accounts list (or via list search) without errors.
- Failure Conditions:
  - Navigation to Accounts fails or times out.
  - The "Ledges" account cannot be found in any reasonable list view or by search.
  - Permission or error banner appears preventing access to Accounts or the record.

### Scenario 2: Navigate to Sales (Leads) and verify the "Robert Anderson" lead exists
- Assumptions:
  - User is logged in and has access to Leads within Sales.
  - A lead named "Robert Anderson" exists.
- Steps:
  1. From any page, ensure the global navigation bar is visible with a link named Sales.
  2. Click the Sales link. Confirm the Sales area loads (typically the Leads list view by default).
  3. Wait for the Leads list view to load (e.g., ensure any "Loading..." text disappears and the grid is visible).
  4. Observe the active list view (often "Recently Viewed"). If the target record is not visible:
     - Option A: Use the search within the list view to search for "Robert Anderson".
     - Option B: Switch to a broader list view (e.g., "All Open Leads"), then search if needed.
  5. Verify a link named "Robert Anderson" is visible in the grid.
  6. Optional: Click the "Robert Anderson" link to open the record detail page and validate the record header shows "Robert Anderson".
- Expected Results:
  - Sales > Leads list is displayed with the grid loaded.
  - A link named "Robert Anderson" is present and visible in the table.
  - Optional: Record detail header reads "Robert Anderson" when opened.
- Success Criteria:
  - The "Robert Anderson" lead link is displayed in the Leads list (or via list search) without errors.
- Failure Conditions:
  - Navigation to Sales/Leads fails or times out.
  - The "Robert Anderson" lead cannot be found in any reasonable list view or by search.
  - Permission or error banner appears preventing access to Leads or the record.

### Scenario 3: Navigate to the Home page
- Assumptions:
  - User is logged in and has access to the Home page.
- Steps:
  1. Click the Home link in the global navigation bar.
  2. Wait for the Home page to load.
  3. Verify the page heading shows "Home".
  4. Optional: Verify the "Recent Records" card is present and loaded. If previously accessed, records such as "Ledges" and/or "Robert Anderson" may appear here.
- Expected Results:
  - Home page loads successfully and displays the Home heading and cards.
- Success Criteria:
  - Home page is visible with core cards or content rendered.
- Failure Conditions:
  - Home page fails to load, shows errors, or navigation is blocked.

### Scenario 4: Close the browser
- Assumptions:
  - The preceding navigation scenarios have completed.
- Steps:
  1. Close the browser/window/tab used for testing.
- Expected Results:
  - The test session ends cleanly without crashes or hangs.
- Success Criteria:
  - Browser closes without error dialogs or lingering processes.
- Failure Conditions:
  - Browser becomes unresponsive or throws errors upon closing.

## Edge Cases and Negative Scenarios
1. Record not present in "Recently Viewed":
   - Use the list view search to query the exact record name ("Ledges" or "Robert Anderson").
   - Switch to a broader list view (e.g., "All Accounts", "All Open Leads") and search.
   - If still not found, log as data issue and verify test data seeding with the team.
2. List view not available or restricted:
   - Attempt alternative standard list views available to the user.
   - Validate user permissions for object visibility.
3. Navigation item missing in the global bar:
   - Confirm you are in the correct app context (e.g., Sales app) via the top navigation.
   - If the tab is customized away for the profile, escalate to admin or use direct object URLs if policy allows.
4. Loading or performance delays:
   - Implement waits for dynamic loaders (e.g., wait for "Loading..." to disappear) and set reasonable timeouts.
   - Retry the Refresh control of the list if supported.
5. Access/permission errors:
   - Capture the error message and affected object.
   - Attempt to access another visible object to confirm scope of issue.
6. Session timeout or login redirect:
   - Re-authenticate and resume the scenario from the last stable checkpoint.

## Validation and Oracles
- Visual oracle: Presence of a link with the exact accessible name "Ledges" in Accounts and "Robert Anderson" in Leads.
- URL oracle: Ensure object list URLs load without error.
- Heading oracle: Confirm correct page headings (e.g., Accounts, Sales/Leads, Home).

## Example Automation Hints (Playwright)
- Navigate to Accounts and verify Ledges
  - await page.getByRole('link', { name: 'Accounts' }).click();
  - await expect(page.getByRole('link', { name: 'Ledges' })).toBeVisible();
- Navigate to Sales and verify Robert Anderson
  - await page.getByRole('link', { name: 'Sales' }).click();
  - await page.getByText('Loading...').first().waitFor({ state: 'hidden' });
  - await expect(page.getByRole('link', { name: 'Robert Anderson' })).toBeVisible();
- Navigate Home
  - await page.getByRole('link', { name: 'Home' }).click();
  - await expect(page.getByRole('heading', { name: 'Home' })).toBeVisible();

## Reporting
- For each scenario, record:
  - Start/end timestamps
  - Pass/Fail and evidence (screenshot/logs if needed)
  - Defects with reproducible steps and environment details

## Exit Criteria
- All four scenarios pass on the target environment.
- No Severity 1/2 defects remain open related to navigation or data visibility.
- Documented deviations (e.g., data gaps) are reviewed and accepted by stakeholders.
