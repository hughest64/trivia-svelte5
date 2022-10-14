import { expect, test } from '@playwright/test';
import { login } from './utils.js';

test.beforeEach( async ({ page }) => {
    await login(page);
});

test('non staff user accessing /host/choice redirects to team', async ({ page }) => {
    await page.goto('/host/choice');
    await expect(page).toHaveURL(/\/team/i);
});

test('non staff user accessing /host/event-setup redirects to team', async ({ page }) => {
    await page.goto('/host/event-setup');
    await expect(page).toHaveURL(/team/i);
});

test('non staff user accessing /host/1234 redirects to team', async ({ page }) => {
    await page.goto('/host/1234');
    await expect(page).toHaveURL(/team/i);
});

// TODO: we can probably modify the auth function to handle an
// alternate expected endpoint and then add tests for /scoring, etc
