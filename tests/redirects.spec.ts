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

// - navigate to login when already logged in
// - navigate to / when already logged in

// test that that /team?next=/abc/123 redirects to the next param
// test sample_admin (or any user w/o an active team)
// - should get redirected to /team with a querystring, don't select a team, or the will be invalid next time
// - test game, leaderboard, megaround, chat, join,
// test expired (or lack of) jwt when connectiong to websocket
// - should be logged out and endup back at login
