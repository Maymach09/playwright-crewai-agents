"""
Knowledge Base Module - Initial RAG Content

This module defines the initial knowledge we seed into our RAG system.
Think of it as the "textbook" our agents learn from.

Structure:
- Fix patterns: Error → Solution mappings
- Code patterns: Reusable Playwright snippets
- Test plans: Templates and strategies
"""

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class KnowledgeItem:
    """
    Single piece of knowledge with context.
    
    Attributes:
        id: Unique identifier
        content: The actual knowledge text
        metadata: Context information
    """
    id: str
    content: str
    metadata: Dict


class InitialKnowledge:
    """
    Initial knowledge base to seed the RAG system.
    
    This is our starting point. As agents work, they'll add
    more knowledge automatically through the feedback loop.
    """
    
    @staticmethod
    def get_test_fixes() -> List[KnowledgeItem]:
        """
        Common test fix patterns.
        
        These are proven solutions to frequent Playwright errors.
        The Healer agent will search these when fixing tests.
        
        Returns:
            List of fix patterns
        """
        return [
            # Locator errors
            KnowledgeItem(
                id="fix_locator_001",
                content="When getting 'locator not found' error, use waitForSelector with timeout. Example: await page.waitForSelector('selector', { timeout: 10000 });",
                metadata={
                    "error_type": "locator",
                    "error_pattern": "locator.*not found",
                    "success_rate": 0.9,
                    "tags": "locator,wait,timeout"
                }
            ),
            KnowledgeItem(
                id="fix_locator_002",
                content="For strict mode violations ('multiple elements'), add { exact: true } or use more specific selector with data-testid. Example: page.locator('[data-testid=\"unique-id\"]')",
                metadata={
                    "error_type": "locator",
                    "error_pattern": "strict mode violation|multiple elements",
                    "success_rate": 0.95,
                    "tags": "locator, strict, specificity"
                }
            ),
            KnowledgeItem(
                id="fix_locator_003",
                content="When element is not visible, use waitForLoadState before interaction. Example: await page.waitForLoadState('networkidle'); then interact.",
                metadata={
                    "error_type": "visibility",
                    "error_pattern": "not visible|hidden|detached",
                    "success_rate": 0.85,
                    "tags": "visibility, wait, timing"
                }
            ),
            
            # Timeout errors
            KnowledgeItem(
                id="fix_timeout_001",
                content="For timeout errors, increase timeout and add explicit waits. Example: await page.waitForSelector('selector', { state: 'visible', timeout: 30000 });",
                metadata={
                    "error_type": "timeout",
                    "error_pattern": "timeout.*exceeded",
                    "success_rate": 0.8,
                    "tags": "timeout, wait, performance"
                }
            ),
            KnowledgeItem(
                id="fix_timeout_002",
                content="If navigation timeout occurs, wait for specific network events. Example: await page.waitForLoadState('domcontentloaded'); or await page.waitForLoadState('networkidle');",
                metadata={
                    "error_type": "timeout",
                    "error_pattern": "navigation.*timeout",
                    "success_rate": 0.75,
                    "tags": "navigation, timeout, network"
                }
            ),
            
            # State management
            KnowledgeItem(
                id="fix_state_001",
                content="For authentication errors, ensure auth_state.json is loaded before navigation. Example: await context.addCookies(authState.cookies); await context.addInitScript(() => { localStorage.setItem('key', 'value'); });",
                metadata={
                    "error_type": "authentication",
                    "error_pattern": "not authenticated|login required",
                    "success_rate": 0.95,
                    "tags": "auth, state, cookies"
                }
            ),
            
            # Interaction errors
            KnowledgeItem(
                id="fix_interaction_001",
                content="For 'element is not enabled' errors, wait for element to be enabled. Example: await page.locator('button').waitFor({ state: 'enabled' }); await page.locator('button').click();",
                metadata={
                    "error_type": "interaction",
                    "error_pattern": "not enabled|disabled",
                    "success_rate": 0.9,
                    "tags": "interaction, state, wait"
                }
            ),
            KnowledgeItem(
                id="fix_interaction_002",
                content="For click interception errors, use force: true or scroll into view first. Example: await page.locator('button').scrollIntoViewIfNeeded(); await page.locator('button').click();",
                metadata={
                    "error_type": "interaction",
                    "error_pattern": "click.*intercepted|covered by",
                    "success_rate": 0.85,
                    "tags": "click, scroll, overlay"
                }
            ),
            
            # Assertion errors
            KnowledgeItem(
                id="fix_assertion_001",
                content="For assertion failures, add soft assertions with expect.soft() or increase wait time before assertion. Example: await expect.soft(locator).toBeVisible({ timeout: 10000 });",
                metadata={
                    "error_type": "assertion",
                    "error_pattern": "assertion failed|expected.*but got",
                    "success_rate": 0.8,
                    "tags": "assertion, expect, wait"
                }
            ),
        ]
    
    @staticmethod
    def get_code_patterns() -> List[KnowledgeItem]:
        """
        Reusable Playwright code patterns.
        
        The Generator agent uses these as templates
        when creating new tests.
        
        Returns:
            List of code patterns
        """
        return [
            # Navigation patterns
            KnowledgeItem(
                id="pattern_nav_001",
                content="""// Navigate with authentication
import { test, expect } from '@playwright/test';
import authState from './auth_state.json';

test.use({ storageState: authState });

test('navigate to page', async ({ page }) => {
  await page.goto('https://example.com/path');
  await page.waitForLoadState('networkidle');
  await expect(page).toHaveURL(/.*path.*/);
});""",
                metadata={
                    "pattern_type": "navigation",
                    "complexity": "simple",
                    "tags": "navigation, auth, basic"
                }
            ),
            
            # Form patterns
            KnowledgeItem(
                id="pattern_form_001",
                content="""// Fill and submit form
await page.locator('[data-testid="input-field"]').fill('value');
await page.locator('select[name="dropdown"]').selectOption('option');
await page.locator('[type="checkbox"]').check();
await page.locator('button[type="submit"]').click();
await page.waitForLoadState('networkidle');""",
                metadata={
                    "pattern_type": "form",
                    "complexity": "simple",
                    "tags": "form, input, submit"
                }
            ),
            
            # Wait patterns
            KnowledgeItem(
                id="pattern_wait_001",
                content="""// Robust wait strategies
// Wait for element
await page.waitForSelector('[data-testid="element"]', { 
  state: 'visible', 
  timeout: 10000 
});

// Wait for network
await page.waitForLoadState('networkidle');

// Wait for specific response
await page.waitForResponse(response => 
  response.url().includes('/api/') && response.status() === 200
);""",
                metadata={
                    "pattern_type": "wait",
                    "complexity": "medium",
                    "tags": "wait, async, timing"
                }
            ),
            
            # Assertion patterns
            KnowledgeItem(
                id="pattern_assert_001",
                content="""// Common assertions
await expect(page.locator('[data-testid="element"]')).toBeVisible();
await expect(page.locator('[data-testid="element"]')).toHaveText('Expected');
await expect(page).toHaveURL(/.*expected-path.*/);
await expect(page.locator('[data-testid="count"]')).toHaveCount(5);""",
                metadata={
                    "pattern_type": "assertion",
                    "complexity": "simple",
                    "tags": "assertion, expect, validation"
                }
            ),
            
            # Locator patterns
            KnowledgeItem(
                id="pattern_locator_001",
                content="""// Best practice locators (in order of preference)
// 1. data-testid (most reliable)
page.locator('[data-testid="unique-id"]')

// 2. Role + name (accessible)
page.getByRole('button', { name: 'Submit' })

// 3. Text content
page.getByText('Specific Text', { exact: true })

// 4. Placeholder
page.getByPlaceholder('Enter email')

// 5. Label
page.getByLabel('Email Address')""",
                metadata={
                    "pattern_type": "locator",
                    "complexity": "simple",
                    "tags": "locator, selector, best-practice"
                }
            ),
        ]
    
    @staticmethod
    def get_test_plan_templates() -> List[KnowledgeItem]:
        """
        Test planning templates and strategies.
        
        The Planner agent uses these to structure
        comprehensive test scenarios.
        
        Returns:
            List of planning templates
        """
        return [
            KnowledgeItem(
                id="plan_smoke_001",
                content="""Smoke test structure:
1. Navigate to application
2. Verify key elements visible
3. Check authentication state
4. Test critical user path (happy path)
5. Verify no console errors
Focus: Fast execution, core functionality only""",
                metadata={
                    "plan_type": "smoke",
                    "test_level": "basic",
                    "tags": "smoke, quick, critical-path"
                }
            ),
            KnowledgeItem(
                id="plan_e2e_001",
                content="""End-to-end test structure:
1. Setup: Authentication, data preparation
2. Navigate to starting point
3. Execute user workflow (multiple steps)
4. Validate each step's outcome
5. Verify final state
6. Cleanup: Reset data if needed
Focus: Complete user journey, realistic scenario""",
                metadata={
                    "plan_type": "e2e",
                    "test_level": "comprehensive",
                    "tags": "e2e, workflow, integration"
                }
            ),
            KnowledgeItem(
                id="plan_crud_001",
                content="""CRUD test structure:
1. Create: Add new entity, verify creation
2. Read: Navigate to entity, verify details
3. Update: Modify entity, verify changes
4. Delete: Remove entity, verify removal
5. Negative: Test validation rules
Focus: Complete lifecycle of data entity""",
                metadata={
                    "plan_type": "crud",
                    "test_level": "comprehensive",
                    "tags": "crud, data, lifecycle"
                }
            ),
            KnowledgeItem(
                id="plan_navigation_001",
                content="""Navigation test structure:
1. Test direct URL navigation
2. Test navigation via UI elements (buttons, links)
3. Verify URL updates correctly
4. Verify page content loads
5. Test browser back/forward
6. Verify authentication persists
Focus: Application routing and state management""",
                metadata={
                    "plan_type": "navigation",
                    "test_level": "medium",
                    "tags": "navigation, routing, state"
                }
            ),
        ]
    
    @staticmethod
    def get_application_knowledge() -> List[KnowledgeItem]:
        """
        Initial application knowledge seeds.
        
        This collection stores discovered UI elements, flows, and
        application structure. Over time, it builds up an "application map".
        
        Returns:
            List of application knowledge patterns
        """
        return [
            # Example: Initial Salesforce knowledge
            KnowledgeItem(
                id="app_salesforce_001",
                content="""Salesforce Account Creation Flow:
Navigation: Home → Accounts → New button
Required Fields: Account Name (textbox)
Optional Fields: Phone (textbox), Website (textbox)
Actions: Save button (creates record), Cancel button (discards)
Success Indicator: URL changes to /lightning/r/Account/[id]/view
Locators: 
- Accounts link: getByRole('link', { name: 'Accounts', exact: true })
- New button: getByRole('button', { name: 'New' })
- Account Name: getByRole('textbox', { name: 'Account Name', exact: true })
- Save: getByRole('button', { name: 'Save', exact: true })""",
                metadata={
                    "application": "salesforce",
                    "module": "accounts",
                    "action": "create",
                    "last_verified": "2024-01-01",
                    "tags": "salesforce, accounts, create, form"
                }
            ),
        ]
    
    @staticmethod
    def get_all_knowledge() -> Dict[str, List[KnowledgeItem]]:
        """
        Get all initial knowledge organized by collection.
        
        Returns:
            Dict mapping collection names to knowledge items
        """
        return {
            "test_fixes": InitialKnowledge.get_test_fixes(),
            "code_patterns": InitialKnowledge.get_code_patterns(),
            "test_plans": InitialKnowledge.get_test_plan_templates(),
            "application_knowledge": InitialKnowledge.get_application_knowledge()
        }
