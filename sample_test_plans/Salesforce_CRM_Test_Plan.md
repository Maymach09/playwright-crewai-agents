# Salesforce CRM Application - Comprehensive Test Plan

## Application Overview

The Salesforce CRM application is a cloud-based customer relationship management platform that provides comprehensive sales, service, and marketing functionality. The application features:

- **Navigation Structure**: Top-level navigation with Home, Contacts, Accounts, Sales, Service, Marketing, Commerce, Generative Canvas, and Your Account modules
- **Account Management**: Complete account lifecycle management with creation, viewing, editing, and relationship tracking
- **Lead Management**: Lead capture, conversion, and pipeline management within the Sales module
- **Dashboard & Analytics**: Home dashboard with configurable widgets showing leads, opportunities, contacts, and recent records
- **User Interface**: Modern Lightning Experience with intuitive navigation, forms, and list views
- **Record Management**: Standard Salesforce objects with full CRUD operations and relationship management

## Test Scenarios

### 1. Account Creation and Management

**Seed:** `tests/seed.spec.ts`

#### 1.1 Navigate to Accounts Module
**Steps:**
1. Open Salesforce application (starting from Home page)
2. Click on "Accounts" tab in the main navigation menu
3. Verify the Accounts list view loads

**Expected Results:**
- URL changes to `/lightning/o/Account/list?filterName=Recent`
- Page title displays "Recently Viewed | Accounts | Salesforce"
- Accounts list view displays with existing account "Ledges"
- "New" button is visible and clickable
- List view controls are available (Search, Refresh, Edit List)

#### 1.2 Create New Account with Complete Information
**Steps:**
1. From Accounts list view, click "New" button
2. Verify "New Account" dialog opens
3. Fill in required field: Account Name = "TechSolutions Corp"
4. Fill in optional fields:
   - Website = "https://techsolutions.com"
   - Type = Select "Customer" from dropdown
   - Description = "Leading technology solutions provider"
   - Phone = "+1-555-123-4567"
   - Billing Address:
     - Billing Country = "United States"
     - Billing Street = "123 Main Street"
     - Billing City = "San Francisco"
     - Billing State/Province = "California"
     - Billing Zip/Postal Code = "94102"
5. Click "Save" button

**Expected Results:**
- New Account dialog opens with all form sections visible (About, Get in Touch)
- Required fields are marked with red asterisk (*)
- All form fields accept input correctly
- Account is successfully created
- User is redirected to the new account's detail page
- Account appears in Recently Viewed accounts list

#### 1.3 Create Account with Minimal Required Information
**Steps:**
1. Navigate to Accounts list view
2. Click "New" button
3. Fill only required field: Account Name = "Minimal Account"
4. Click "Save" button

**Expected Results:**
- Account is created successfully with only the account name
- All optional fields remain empty
- Account appears in the accounts list
- Account detail page loads correctly

#### 1.4 Account Creation Validation - Missing Required Field
**Steps:**
1. Navigate to Accounts list view
2. Click "New" button
3. Leave Account Name field empty
4. Fill optional fields (Website, Phone)
5. Attempt to click "Save" button

**Expected Results:**
- Save operation fails
- Error message indicates Account Name is required
- Form remains open with entered data preserved
- User can correct the error and retry

#### 1.5 Cancel Account Creation
**Steps:**
1. Navigate to Accounts list view
2. Click "New" button
3. Fill in some form fields
4. Click "Cancel" button or "Cancel and close" (X) button

**Expected Results:**
- New Account dialog closes
- No new account is created
- User returns to Accounts list view
- No data is saved

### 2. Lead Creation and Management

**Seed:** `tests/seed.spec.ts`

#### 2.1 Navigate to Sales Module
**Steps:**
1. From Home page, click on "Sales" tab in the main navigation
2. Verify the Sales module loads and displays Leads section by default

**Expected Results:**
- URL changes to `/lightning/o/Lead/list?filterName=Recent`
- Page title displays "Recently Viewed | Leads | Salesforce"
- Leads list view displays with existing lead "Robert Anderson"
- Sales navigation shows Leads, Contacts, Accounts, Opportunities, Products, Price Books, Calendar, and Analytics
- "New" button is available for lead creation

#### 2.2 Create New Lead with Complete Information
**Steps:**
1. From Leads list view, click "New" button
2. Verify "New Lead" dialog opens
3. Fill in required fields:
   - Salutation = "Ms." from dropdown
   - First Name = "Sarah"
   - Last Name = "Johnson"
   - Company = "Innovation Systems"
   - Lead Status = "New" (default)
4. Fill in optional fields:
   - Title = "Marketing Director"
   - Website = "https://innovationsys.com"
   - Description = "Potential customer for CRM solutions"
   - Phone = "+1-555-987-6543"
   - Email = "sarah.johnson@innovationsys.com"
   - Address:
     - Country = "United States"
     - Street = "456 Innovation Drive"
     - City = "Austin"
     - State/Province = "Texas"
     - Zip/Postal Code = "78701"
   - No. of Employees = "150"
   - Annual Revenue = "5000000"
   - Lead Source = "Web" from dropdown
   - Industry = "Technology" from dropdown
5. Click "Save" button

**Expected Results:**
- New Lead dialog opens with all sections visible (About, Get in Touch, Segment)
- All form fields accept appropriate input
- Dropdown fields display available options
- Lead is successfully created
- User is redirected to the new lead's detail page
- Lead appears in Recently Viewed leads list

#### 2.3 Create Lead with Minimal Required Information
**Steps:**
1. Navigate to Leads list view
2. Click "New" button
3. Fill only required fields:
   - Last Name = "Smith"
   - Company = "Basic Corp"
4. Click "Save" button

**Expected Results:**
- Lead is created successfully with minimal information
- Default values are applied (Lead Status = "New")
- Lead Owner is automatically assigned to current user
- Lead appears in the leads list

#### 2.4 Lead Creation Validation - Missing Required Fields
**Steps:**
1. Navigate to Leads list view
2. Click "New" button
3. Fill only First Name = "John"
4. Leave Last Name and Company fields empty
5. Attempt to click "Save" button

**Expected Results:**
- Save operation fails
- Error messages indicate required fields (Last Name, Company)
- Form remains open with entered data preserved
- User can correct errors and retry

#### 2.5 Use Save & New Function
**Steps:**
1. Navigate to Leads list view
2. Click "New" button
3. Fill required fields for first lead:
   - Last Name = "Wilson"
   - Company = "Wilson Enterprises"
4. Click "Save & New" button
5. Fill required fields for second lead:
   - Last Name = "Brown"
   - Company = "Brown Industries"
6. Click "Save" button

**Expected Results:**
- First lead is saved successfully
- New Lead dialog remains open and is cleared for next entry
- Second lead is saved successfully
- Both leads appear in the leads list

### 3. Navigation and User Experience

**Seed:** `tests/seed.spec.ts`

#### 3.1 Home Page Navigation and Dashboard
**Steps:**
1. Start from any page in the application
2. Click "Home" in the main navigation
3. Verify all dashboard components load

**Expected Results:**
- URL changes to `/lightning/page/home`
- Page title displays "Home | Salesforce"
- Dashboard displays welcome message with user name
- Report widgets are visible: Leads, Opportunities, Contacts, Cases
- Recent Records section shows recent activities
- Navigation suggestions are displayed
- All report widgets show appropriate data or "View Report" links

#### 3.2 Cross-Module Navigation Flow
**Steps:**
1. Start from Home page
2. Navigate to Accounts module
3. Navigate to Sales (Leads) module
4. Return to Home page

**Expected Results:**
- Each navigation action loads the correct module
- Page URLs and titles update appropriately
- Navigation state is maintained correctly
- No broken links or loading errors occur
- User can seamlessly move between modules

#### 3.3 Search Functionality
**Steps:**
1. Navigate to Accounts list view
2. Use the search box to search for "Ledges"
3. Navigate to Leads list view
4. Use the search box to search for "Robert"

**Expected Results:**
- Search box is visible and functional in both list views
- Search results filter the displayed records appropriately
- Search functionality works as expected for existing records

### 4. Form Validation and Error Handling

**Seed:** `tests/seed.spec.ts`

#### 4.1 Account Form Field Validation
**Steps:**
1. Navigate to Accounts and click "New"
2. Test field length limits by entering very long text in Account Name
3. Test website field with invalid URL format
4. Test phone field with invalid phone number format
5. Attempt to save with various invalid combinations

**Expected Results:**
- Form provides appropriate validation messages
- Field length limits are enforced
- Format validation works for specialized fields
- User receives clear guidance on how to fix errors

#### 4.2 Lead Form Field Validation
**Steps:**
1. Navigate to Sales/Leads and click "New"
2. Test email field with invalid email format
3. Test numeric fields (employees, revenue) with non-numeric input
4. Test required field validation for various combinations
5. Verify dropdown field behavior

**Expected Results:**
- Email validation prevents invalid email formats
- Numeric fields only accept appropriate numeric input
- Required field validation is consistent
- Dropdown fields only accept valid selections

### 5. Data Persistence and Record Management

**Seed:** `tests/seed.spec.ts`

#### 5.1 Verify Created Records Persist
**Steps:**
1. Create a new account with complete information
2. Navigate away from Accounts to another module
3. Return to Accounts list view
4. Verify the created account is still visible
5. Click on the account to view details

**Expected Results:**
- Created account persists after navigation
- Account details are saved correctly
- Account appears in Recently Viewed list
- All entered data is preserved accurately

#### 5.2 Record Relationship and Reference
**Steps:**
1. Create an account
2. Navigate to Leads and create a lead
3. Note the relationships and references between records
4. Verify recent records section on Home page updates

**Expected Results:**
- Records are properly created and linked
- Recent Records section reflects new activities
- Record relationships are maintained
- Data integrity is preserved

### 6. Browser and Session Management

**Seed:** `tests/seed.spec.ts`

#### 6.1 Application Stability
**Steps:**
1. Perform multiple create operations in sequence
2. Navigate between modules multiple times
3. Use browser back/forward buttons
4. Open multiple dialogs and cancel them

**Expected Results:**
- Application remains stable during extended use
- No memory leaks or performance degradation
- Browser navigation works as expected
- Modal dialogs behave consistently

#### 6.2 Session and State Management
**Steps:**
1. Create records and navigate between modules
2. Refresh the browser page
3. Verify application state is maintained

**Expected Results:**
- Application handles browser refresh gracefully
- User session is maintained
- No data loss occurs during refresh
- Application returns to appropriate state

## Test Execution Notes

### Prerequisites
- Valid Salesforce org with appropriate permissions
- User must have Create, Read, Edit permissions on Account and Lead objects
- Test data should be cleaned up after test execution
- Tests should be independent and not rely on specific existing data

### Test Data Management
- Use unique, identifiable test data (e.g., timestamps in names)
- Clean up test records after scenario completion when possible
- Verify existing test data (Ledges account, Robert Anderson lead) before starting
- Tests should handle both empty and populated list views

### Success Criteria
- All scenarios execute without errors
- Data is created and persisted correctly
- Navigation functions as expected
- Form validation works appropriately
- User experience is smooth and intuitive

### Failure Handling
- Document any unexpected errors or behaviors
- Capture screenshots of failed states when possible
- Note specific error messages and conditions
- Verify if failures are environmental or functional

## Risk Considerations

### High Risk Areas
- Form validation and required field handling
- Data persistence across navigation
- Cross-module integration and references
- Browser compatibility and session management

### Medium Risk Areas
- Search functionality accuracy
- Dashboard widget loading and data display
- Modal dialog behavior and state management
- User permissions and access control

### Low Risk Areas
- Basic navigation between modules
- Static content display
- Standard Salesforce Lightning UI components
- Help text and tooltip functionality