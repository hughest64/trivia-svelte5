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

// player side redirect and login to specific endpoints
test('proper redirect for game home page', async ({ page }) => authRedirects(page, '/team'));
test('proper redirect for game join page', async ({ page }) => authRedirects(page, '/game/join'));
test('proper redirect for game page', async ({ page }) => authRedirects(page, '/game/1234'));

// host side redirect and login to specific endpoints
// TODO: do we test non-staff redirects too?
// host/event-setup
// host/1234

// TODO:
// - login test (fill in form) - we do this a log alredy?
// - logout test
// - navigate to login when already logged in (as player and host)
