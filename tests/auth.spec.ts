import { expect, test } from '@playwright/test';
import { authRedirects } from './utils.js';

// test guest login
test('guest/not-staff login from redirect', async ({ page }) => {
    await page.goto('/');
    // not logged in, we should land on the welcome page
    await expect(page).toHaveTitle(/welcome/i);
    // click to log in as a guest
    await page.locator('text=Play as a Guest').click();
    // since guest is not a staff user, they should see the team select component
    await expect(page).toHaveTitle(/team select/i);
    expect(await page.textContent('h1')).toBe('Create a New Team');
});

// redirect and login of other routes
test('proper redirect for game home page', async ({ page }) => authRedirects(page, '/'));
test('proper redirect for game join page', async ({ page }) => authRedirects(page, '/game/join'));
test('proper redirect for game game page', async ({ page }) => authRedirects(page, '/game/1234'));
