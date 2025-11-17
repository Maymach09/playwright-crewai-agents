# Salesforce Account Management - Comprehensive Test Plan

## Application Overview

This test plan covers the Salesforce Lightning Experience application, specifically focusing on account management workflows. The application provides:

- **Authentication**: Secure login with email and password credentials, with 2FA support
- **Navigation**: Lightning Experience interface with global navigation bar and app launcher
- **Account Management**: Full CRUD operations on account records
- **Account Details**: Comprehensive account information including Type, Name, Contact information, and History
- **Session Management**: Persistent authentication state and logout functionality

**Test Environment**: https://nosoftware-saas-2365.my.salesforce.com/

**Test Credentials**:
- Email: mayank.mahajan0-4f6b@force.com
- Password: Sales@090985

**Authentication State File**: `auth_state.json` (for bypassing login in tests)

---

## Test Scenarios

### 1. Authentication and Session Management

**Assumption**: Starting from a logged-out state OR using existing authenticated session.

#### 1.1 Login with Valid Credentials

**Steps**:
1. Navigate to https://nosoftware-saas-2365.my.salesforce.com/
2. If presented with login page, enter email: mayank.mahajan0-4f6b@force.com
3. Click "Continue" or "Next" button
4. Enter password: Sales@090985
5. Click "Log In" button
6. **If 2FA prompt appears**: PAUSE and wait for user to provide the verification code
7. After receiving code from user, enter the 2FA code
8. Submit the 2FA code

**Expected Results**:
- User is successfully authenticated
- Application redirects to Salesforce Home page
- User sees global navigation header with Home logo, Search bar, and user profile icon
- Main navigation sidebar displays app modules (Home, Contacts, Accounts, Sales, Service, Marketing, Commerce, etc.)
- Home page displays welcome message with user's first name
- No error messages are displayed

**Success Criteria**:
- URL changes to `/lightning/page/home` or similar Lightning Experience URL
- User profile icon is visible in top-right corner
- Navigation menu is accessible and populated

---

#### 1.2 Use Existing Session (Auth State Bypass)

**Purpose**: Skip login process by using pre-authenticated session state.

**Test Setup**:
```typescript
test.use({ storageState: 'auth_state.json' });
```

**Steps**:
1. Configure test to use stored authentication state file `auth_state.json`
2. Navigate to https://nosoftware-saas-2365.my.salesforce.com/

**Expected Results**:
- Application directly loads to authenticated state
- No login page is displayed
- User lands on Salesforce Home page
- All authenticated features are immediately accessible

**Success Criteria**:
- Login page is bypassed completely
- Session is valid and active
- User can perform authenticated actions without re-entering credentials

---

#### 1.3 Handle 2FA Authentication

**Assumption**: Starting from login page where 2FA is required.

**Steps**:
1. Complete standard login (Steps 1-5 from scenario 1.1)
2. System displays 2FA verification prompt
3. PAUSE automation and display message: "2FA code required. Please provide the verification code."
4. Wait for user input
5. Once user provides code, enter the verification code in the input field
6. Click "Verify" or "Submit" button

**Expected Results**:
- 2FA prompt is displayed after password entry
- Code input field accepts numeric verification code
- Upon successful verification, user is redirected to Home page
- Invalid code displays appropriate error message

**Success Criteria**:
- System correctly prompts for 2FA when required
- Automation can pause and resume after receiving user input
- Valid codes are accepted and authentication completes
- Invalid codes are rejected with clear error messaging

---

### 2. Accounts Module Navigation

**Assumption**: Starting from authenticated Salesforce Home page.

#### 2.1 Navigate to Accounts Module

**Steps**:
1. From Salesforce Home page, locate the main navigation sidebar on the left
2. Click on "Accounts" link in the navigation menu

**Expected Results**:
- Page navigates to Accounts list view
- URL changes to `/lightning/o/Account/list?filterName=Recent`
- Page displays "Accounts" heading
- "Recently Viewed" filter is active by default
- Account list table is displayed with columns: Account Name, Phone, Account Owner Alias, Action
- Action buttons visible: "New", "Import", "Assign Label"
- List view controls are available: Search, Refresh, Display options

**Success Criteria**:
- Accounts list view loads successfully
- At least the Recently Viewed accounts are displayed (if any exist)
- Interface is fully interactive and responsive

---

#### 2.2 View Recently Viewed Accounts List

**Assumption**: Starting from Accounts list view.

**Steps**:
1. On the Accounts page, verify "Recently Viewed" filter is selected
2. Observe the accounts list table
3. Check for item count display (e.g., "1 item • Updated a few seconds ago")

**Expected Results**:
- List displays accounts that were recently accessed
- Each account row shows: Item Number, Checkbox, Account Name (clickable), Phone, Account Owner Alias, Actions menu
- Item count is displayed above the table
- Last updated timestamp is shown
- If no accounts exist, appropriate empty state message is displayed

**Success Criteria**:
- Recently accessed accounts are listed correctly
- Account information is accurate and complete
- List view provides clear visual hierarchy

---

### 3. Account Detail Operations

**Assumption**: Starting from Accounts list view with at least one account (Ledges) available.

#### 3.1 Open Ledges Account

**Steps**:
1. From the Accounts list view, locate the "Ledges" account in the list
2. Click on the "Ledges" hyperlink in the Account Name column

**Expected Results**:
- Page navigates to Ledges account detail page
- URL changes to `/lightning/r/Account/{AccountId}/view`
- Page title displays "Ledges | Account | Salesforce"
- Account header shows "Account Ledges" heading
- Action buttons visible: "New Contact", "New Opportunity", "Edit", "Show more actions", "View Account Hierarchy"
- Account details are displayed in sections: About, Get in Touch, History
- Activity Publisher is visible with options: Email, New Event, Log a Call, New Task
- Related lists are displayed: Contacts (0), Opportunities (0), Cases (0), Files (0)

**Success Criteria**:
- Account detail page loads completely
- All account information is displayed correctly
- Page layout matches Lightning Experience standard account layout
- Navigation breadcrumb shows: Accounts > Ledges

---

#### 3.2 View Account Details - About Section

**Assumption**: Starting from Ledges account detail page.

**Steps**:
1. Scroll to the "About" section (usually displayed prominently on the left side)
2. Verify the "About" section is expanded
3. Review displayed fields

**Expected Results**:
- About section displays the following fields:
  - **Account Name**: Ledges (with Edit button)
  - **Website**: (empty or populated, with Edit button)
  - **Type**: Analyst (with Edit button)
  - **Description**: (empty or populated, with Edit button)
  - **Parent Account**: (empty or populated, with Edit button)
  - **Account Owner**: Mayank Mahajan (with "Change Owner" button)
- Each editable field has a pencil icon or "Edit" button
- Read-only fields display their values clearly

**Success Criteria**:
- All expected fields are present and visible
- Current Type value "Analyst" is displayed
- Field values are accurate and match the account record

---

#### 3.3 Edit Account Type Field - View Available Options

**Assumption**: Starting from Ledges account detail page with About section visible.

**Steps**:
1. Locate the "Type" field in the About section (currently showing "Analyst")
2. Click the "Edit Type" button (pencil icon) next to the Type field
3. Observe that the page enters edit mode
4. Click on the Type dropdown/combobox field
5. Review all available Type options in the dropdown

**Expected Results**:
- Clicking "Edit Type" puts the Type field into edit mode
- Type field changes to a combobox/dropdown control
- Current value "Analyst" is pre-selected in the dropdown
- Dropdown displays the following options:
  - --None--
  - Analyst (currently selected)
  - Competitor
  - Customer
  - Integrator
  - Investor
  - Partner
  - Press
  - Prospect
  - Reseller
  - Other
- Required field indicator (*) is shown if Type is required
- "Cancel" and "Save" buttons appear at the bottom of the edit form

**Success Criteria**:
- Edit mode activates successfully
- All Type picklist values are available for selection
- Dropdown is interactive and allows selection

---

#### 3.4 Change Account Type and Save

**Assumption**: Starting from Ledges account detail page with Type field in edit mode.

**Steps**:
1. With the Type field in edit mode (from scenario 3.3), click on the Type dropdown
2. Select a different value from the dropdown (e.g., "Customer")
3. Click the "Save" button at the bottom of the form
4. Wait for save operation to complete

**Expected Results**:
- Selected value is highlighted in the dropdown
- "Save" button becomes enabled
- Upon clicking Save:
  - Loading indicator or spinner appears briefly
  - Success message is displayed (e.g., "Account 'Ledges' was saved")
  - Page returns to view mode
  - Type field now displays the newly selected value (e.g., "Customer")
  - Last Modified By timestamp is updated to current date/time
  - Last Modified By user shows current user (Mayank Mahajan)

**Success Criteria**:
- Type value changes successfully
- Changes are persisted to the database
- Success confirmation is displayed
- Page reflects updated values immediately

---

#### 3.5 Cancel Account Edit

**Assumption**: Starting from Ledges account detail page with any field in edit mode.

**Steps**:
1. Click "Edit Type" or any other edit button to enter edit mode
2. Make a change to the Type field (select a different value)
3. Click the "Cancel" button at the bottom of the form
4. Observe the result

**Expected Results**:
- Clicking Cancel exits edit mode immediately
- Page returns to view mode
- Original Type value is displayed (no changes saved)
- No success or error messages are shown
- Account details remain unchanged

**Success Criteria**:
- Cancel operation works correctly
- No data is modified in the system
- User can safely exit edit mode without saving

---

#### 3.6 Verify Account History Information

**Assumption**: Starting from Ledges account detail page.

**Steps**:
1. Scroll down to locate the "History" section
2. Verify the History section is expanded
3. Review the displayed history fields

**Expected Results**:
- History section displays:
  - **Created By**: User name link (e.g., "Mayank Mahajan") + creation timestamp (e.g., "10/31/2025, 9:19 AM")
  - **Last Modified By**: User name link (e.g., "Mayank Mahajan") + modification timestamp (e.g., "10/31/2025, 9:19 AM")
- User names are clickable links that navigate to user detail pages
- Hover preview icon appears next to user names
- Timestamps are formatted correctly (MM/DD/YYYY, HH:MM AM/PM)

**Success Criteria**:
- History information is accurate
- Created By and Last Modified By reflect actual audit data
- Timestamps update correctly after modifications

---

### 4. Navigation and Return to Home

**Assumption**: Starting from any page within the Salesforce application (e.g., Ledges account detail page).

#### 4.1 Navigate to Home Using Sidebar

**Steps**:
1. Locate the main navigation sidebar on the left side of the page
2. Click on "Home" link in the navigation menu

**Expected Results**:
- Page navigates to Salesforce Home page
- URL changes to `/lightning/page/home` or `/lightning/app/{appId}`
- Home page displays with dashboard widgets and suggestions
- Welcome message displays user's first name
- Recent Records section shows recently accessed items

**Success Criteria**:
- Navigation completes successfully
- Home page loads completely with all widgets
- No errors are displayed

---

#### 4.2 Navigate to Home Using Logo

**Steps**:
1. From any page, locate the Salesforce logo/Home link in the top-left corner of the header
2. Click on the Home logo/link

**Expected Results**:
- Page navigates to Salesforce Home page
- Same results as scenario 4.1

**Success Criteria**:
- Logo click functions as Home navigation
- Consistent with scenario 4.1 results

---

### 5. User Profile and Logout

**Assumption**: Starting from any page within the authenticated Salesforce application.

#### 5.1 Access User Profile Menu

**Steps**:
1. Locate the user profile icon in the top-right corner of the page header (in the Global Header navigation)
2. Click on the "View profile" button (avatar/profile icon)

**Expected Results**:
- User profile dropdown menu opens
- Menu displays:
  - User name heading: "Mayank Mahajan"
  - Organization name: "nosoftware-saas-2365.my.salesforce.com"
  - "Settings" link
  - "Log Out" link
  - Display Density options: Comfy (selected), Compact
  - "Add Username" link
- Menu appears as an overlay/modal on top of the current page

**Success Criteria**:
- Profile menu opens successfully
- All menu items are visible and accessible
- User information is displayed correctly

---

#### 5.2 Logout from Application

**Steps**:
1. Click on the "View profile" button to open the user profile menu (from scenario 5.1)
2. Locate the "Log Out" link in the profile dropdown
3. Click on "Log Out"
4. Wait for logout process to complete

**Expected Results**:
- Clicking "Log Out" initiates the logout process
- Session is terminated
- User is redirected to the Salesforce login page
- URL changes to `/secur/logout.jsp` and then redirects to login page
- All authenticated session data is cleared
- User cannot access authenticated pages without logging in again

**Success Criteria**:
- Logout completes successfully
- Session is fully terminated (no cached authentication)
- Login page displays and accepts new login attempts
- Previously stored session state is invalidated

---

#### 5.3 Verify Logout Persistence

**Assumption**: User has just logged out (completed scenario 5.2).

**Steps**:
1. After logout, attempt to navigate directly to an authenticated page (e.g., Accounts page URL)
2. Observe the system behavior

**Expected Results**:
- System redirects to login page
- User cannot access authenticated content without re-authenticating
- No residual session data allows unauthorized access

**Success Criteria**:
- Security is maintained post-logout
- All authenticated routes require re-authentication

---

## Edge Cases and Error Scenarios

### 6.1 Invalid Login Credentials

**Steps**:
1. Navigate to login page
2. Enter invalid email: invalid@example.com
3. Enter any password
4. Click "Log In"

**Expected Results**:
- Error message displayed: "Please check your username and password"
- User remains on login page
- No authentication occurs

---

### 6.2 Account Type - Deselect Current Value

**Steps**:
1. Edit Ledges account Type field
2. Select "--None--" option from dropdown
3. Click Save

**Expected Results**:
- Type field is cleared
- Account saves successfully with empty Type value
- Field displays as blank/empty in view mode

---

### 6.3 Network Interruption During Save

**Steps**:
1. Edit Ledges account Type field
2. Change the value
3. Simulate network disconnection (if possible in test environment)
4. Click Save

**Expected Results**:
- Error message is displayed indicating save failure
- User is notified to check connection and retry
- Changes are not saved
- User can retry save after network restoration

---

### 6.4 Concurrent Edit Conflict

**Assumption**: Two users attempting to edit the same account simultaneously.

**Steps**:
1. User A opens Ledges account for editing
2. User B opens Ledges account for editing
3. User A changes Type to "Customer" and saves
4. User B changes Type to "Partner" and attempts to save

**Expected Results**:
- User B receives conflict/stale data warning
- System prompts User B to refresh and review latest changes
- User B's changes are not applied until conflict is resolved

---

## Test Data Requirements

### Pre-existing Data:
- **Account**: Ledges (must exist in the system)
  - Current Type: Analyst
  - Account Owner: Mayank Mahajan

### Test Account Credentials:
- **Email**: mayank.mahajan0-4f6b@force.com
- **Password**: Sales@090985
- **2FA**: Available upon request during test execution

### Session State:
- **File**: auth_state.json (stored authentication state for bypassing login)

---

## Test Execution Notes

### Setup Requirements:
1. Ensure `auth_state.json` file exists and contains valid session data
2. Verify test account credentials are active and not locked
3. Ensure "Ledges" account exists in the test environment
4. Confirm 2FA mechanism is configured for the test account

### 2FA Handling Protocol:
When tests encounter 2FA prompts:
1. Test automation should PAUSE execution
2. Display message to test executor: "2FA verification required. Please provide the code."
3. Wait for manual input of 2FA code
4. Resume test execution after code is entered
5. Verify successful authentication before proceeding

### Post-Test Cleanup:
- Reset Ledges account Type field to original value "Analyst" if modified
- Log out from all active sessions
- Archive test execution logs and screenshots

---

## Success Metrics

**Test Coverage Goals**:
- All critical user paths tested: 100%
- Authentication scenarios: Complete
- Account CRUD operations: Complete
- Navigation workflows: Complete
- Logout functionality: Complete

**Pass Criteria**:
- All positive test scenarios pass successfully
- Edge cases are handled gracefully with appropriate error messages
- No unexpected application crashes or errors
- User experience is smooth and intuitive throughout all workflows

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 10/31/2025 | Test Planning Team | Initial comprehensive test plan created |

