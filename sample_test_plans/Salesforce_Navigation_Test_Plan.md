# Salesforce Lightning Experience - Navigation and Data Verification Test Plan

## Application Overview

The Salesforce Lightning Experience is a cloud-based customer relationship management (CRM) platform that provides comprehensive business management functionality. The application features:

- **Navigation System**: Main navigation with tabs for Home, Contacts, Accounts, Sales, Service, Marketing, Commerce, Generative Canvas, and Your Account
- **Home Dashboard**: Centralized dashboard with customizable cards showing leads, opportunities, contacts, cases, and recent records
- **Account Management**: Complete account management with Recently Viewed accounts list and detailed account information
- **Lead Management**: Sales pipeline management with lead tracking, status monitoring, and detailed lead profiles
- **Data Visualization**: Real-time reports and charts for leads, opportunities, contacts, and cases
- **Search & Filter Capabilities**: Global search and list view filtering options
- **Recent Records Tracking**: Quick access to recently viewed records across all modules

## Test Scenarios

### 1. Account Verification and Navigation

**Seed:** `tests/seed.spec.ts`

#### 1.1 Navigate to Accounts Tab and Verify Ledges Account
**Steps:**
1. Start from the Home page of the Salesforce Lightning Experience
2. Click on the "Accounts" tab in the main navigation menu
3. Wait for the Accounts page to load completely
4. Verify that the page title shows "Recently Viewed | Accounts | Salesforce"
5. Verify that the page URL contains "/lightning/o/Account/list?filterName=Recent"
6. Locate the accounts data grid/table
7. Verify that "Ledges" account is visible in the account list

**Expected Results:**
- Page successfully navigates to Accounts section
- Page displays "Accounts Recently Viewed" heading
- Accounts grid shows proper column headers: Item Number, Account Name, Phone, Account Owner Alias, Action
- "Ledges" account appears as a clickable link in the Account Name column
- Status shows "1 item" for Recently Viewed accounts
- Account Owner Alias shows "MMaha" for the Ledges account

#### 1.2 Verify Account List Functionality
**Steps:**
1. From the Accounts page, verify the search functionality is available
2. Check that list view controls are present (Refresh, Edit List, etc.)
3. Verify that "New" button is available for creating new accounts
4. Verify that "Import" and "Assign Label" buttons are present
5. Check that the account grid allows selection with checkboxes

**Expected Results:**
- Search box shows "Search this list..." placeholder
- All control buttons are visible and enabled
- Account selection checkbox is functional
- List view shows proper item count and last updated timestamp

### 2. Sales Module and Lead Verification

#### 2.1 Navigate to Sales Tab and Verify Robert Anderson Lead
**Steps:**
1. From any page in the application, click on the "Sales" tab in the main navigation
2. Wait for the Sales page to load completely
3. Verify that the page navigates to the Leads section by default
4. Verify that the page title shows "Recently Viewed | Leads | Salesforce"
5. Verify that the page URL contains "/lightning/o/Lead/list?filterName=Recent"
6. Locate the leads data grid/table
7. Verify that "Robert Anderson" lead is visible in the leads list

**Expected Results:**
- Page successfully navigates to Sales section showing Leads
- Page displays "Leads Recently Viewed" heading
- Leads grid shows proper column headers: Item Number, Name, Title, Company, Phone, Email, Lead Status, Owner Alias, Action
- "Robert Anderson" appears as a clickable link in the Name column
- Lead shows "Regional Manager" in Title column
- Lead shows "ABC AI" in Company column
- Lead Status shows "New"
- Owner Alias shows "MMaha"

#### 2.2 Verify Sales Module Navigation Options
**Steps:**
1. From the Sales page, verify that the left navigation shows all available sales modules
2. Check that the following options are available: Leads, Contacts, Accounts, Opportunities, Products, Price Books, Calendar, Analytics
3. Verify that each navigation item has an associated list button
4. Verify that action buttons are available: New, Import, Add to Campaign, Send Email, Change Owner

**Expected Results:**
- All sales module navigation items are visible and clickable
- Each module shows appropriate list view option
- Action buttons are properly enabled for lead management
- Status shows "1 item" for Recently Viewed leads

### 3. Home Page Navigation and Dashboard Verification

#### 3.1 Navigate to Home Page and Verify Dashboard Elements
**Steps:**
1. From any page in the application, click on the "Home" tab in the main navigation
2. Wait for the Home page to load completely
3. Verify that the page title shows "Home | Salesforce"
4. Verify that the page URL contains "/lightning/page/home"
5. Verify that the welcome message shows "Welcome, Mayank"
6. Check that suggestion cards are displayed
7. Verify that dashboard reports are visible

**Expected Results:**
- Page successfully navigates to Home dashboard
- Welcome message displays current user name
- Suggestion cards show: "Create your first contact", "Turn on marketing features", "Visualize your data with AI"
- Dashboard shows report sections for Leads, Opportunities, Contacts, and Cases
- Recent Records section displays recent activity including "Ledges" account and "Robert Anderson" lead

#### 3.2 Verify Home Dashboard Report Functionality
**Steps:**
1. From the Home page, verify that the Leads report shows "My Leads" in the dropdown
2. Verify that "Robert Anderson" appears in the leads report grid
3. Check that the Opportunities, Contacts, and Cases report sections are present
4. Verify that each report section has "New" and "View Report" options
5. Check that Recent Records section shows recent items

**Expected Results:**
- Leads report displays with proper data including Robert Anderson
- All report sections show appropriate dropdown selections
- "View Report" links are functional
- Recent Records shows links to "Ledges" account and "Robert Anderson" lead
- Each report shows last updated timestamp

### 4. Application Navigation and User Interface Verification

#### 4.1 Verify Global Navigation Elements
**Steps:**
1. From any page, verify that the global header contains all expected elements
2. Check that the Salesforce Home logo/link is present
3. Verify that the global search functionality is available
4. Check that user profile, notifications, and settings buttons are present
5. Verify that the main navigation menu shows all application modules

**Expected Results:**
- Global header displays consistently across all pages
- Search shows "Search..." placeholder text
- User profile button with tooltip "View profile" is accessible
- Notifications and Quick Settings buttons are present
- Trial information shows "Days left in Starter trial: 27" with "Buy Now" button

#### 4.2 Verify Cross-Module Data Consistency
**Steps:**
1. Navigate to Home page and note "Ledges" in Recent Records
2. Navigate to Accounts page and verify "Ledges" is in the accounts list
3. Navigate to Home page and note "Robert Anderson" in Recent Records and Leads report
4. Navigate to Sales page and verify "Robert Anderson" is in the leads list
5. Verify that data appears consistently across all views

**Expected Results:**
- "Ledges" account appears consistently in Home Recent Records and Accounts list
- "Robert Anderson" lead appears consistently in Home dashboard reports, Recent Records, and Sales leads list
- All record links point to the same record IDs
- Owner information (MMaha) is consistent across all views

### 5. Browser Session and Application State Management

#### 5.1 Verify Application State Persistence
**Steps:**
1. Navigate through different tabs (Home → Accounts → Sales → Home)
2. Verify that each navigation maintains proper application state
3. Check that recently viewed items update appropriately
4. Verify that user session remains active throughout navigation

**Expected Results:**
- Navigation between tabs is smooth and maintains user session
- Recently Viewed lists update to reflect current user activity
- Application maintains proper state without requiring re-authentication
- Page URLs update correctly to reflect current location

#### 5.2 End Session Testing (Browser Close Simulation)
**Steps:**
1. Complete all navigation testing scenarios
2. Verify that all required verifications have been completed
3. Document any observations about application behavior
4. Prepare for browser session termination

**Expected Results:**
- All test scenarios have been completed successfully
- Application functionality works as expected
- No critical errors or broken functionality observed
- Session can be terminated cleanly

## Test Data Requirements

### Pre-existing Test Data
- **Account**: "Ledges" account must exist and be recently viewed
- **Lead**: "Robert Anderson" lead must exist with the following properties:
  - Name: Robert Anderson
  - Title: Regional Manager  
  - Company: ABC AI
  - Status: New
  - Owner: MMaha (current user)

### Test Environment Setup
- Salesforce Lightning Experience instance must be accessible
- User must have appropriate permissions to view Accounts and Leads
- Application should be in a clean state with minimal test data for clear verification

## Success Criteria

### Primary Objectives
✅ **Account Verification**: Successfully navigate to Accounts tab and confirm "Ledges" account is available
✅ **Lead Verification**: Successfully navigate to Sales tab and confirm "Robert Anderson" lead is available  
✅ **Home Navigation**: Successfully navigate to Home page and verify dashboard functionality
✅ **Application Consistency**: Verify that data appears consistently across all modules

### Secondary Objectives
✅ **Navigation Functionality**: All main navigation tabs work correctly
✅ **User Interface Elements**: All buttons, links, and controls function as expected
✅ **Data Integrity**: Cross-module data consistency is maintained
✅ **Session Management**: Application maintains proper user session state

## Risk Considerations

### Potential Issues
- **Data Dependencies**: Test requires specific accounts and leads to exist
- **User Permissions**: Test user must have access to all required modules
- **Network Connectivity**: Stable internet connection required for Salesforce access
- **Browser Compatibility**: Testing should be performed on supported browsers

### Mitigation Strategies
- Verify test data exists before beginning test execution
- Confirm user permissions in test environment setup
- Include network connectivity checks in test prerequisites
- Document browser version and configuration used for testing

## Execution Notes

- **Test Duration**: Approximately 5-10 minutes for complete execution
- **Prerequisites**: Valid Salesforce login credentials and test data setup
- **Dependencies**: None (tests can be run independently)
- **Automation Potential**: High - All scenarios are suitable for automated testing
- **Maintenance**: Regular updates needed if UI elements or test data change