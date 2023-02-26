import { expect, test } from '@playwright/test';
import { login } from './utils.js';

const playerSelectedTeam = 'hello world';

test.describe('a player cannot access host endpoints', async () => {
    test.beforeEach(async ({ page }) => {
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

    test('non staff user accessing /host/1234/chat redirects to team', async ({ page }) => {
        await page.goto('/host/1234/chat');
        await expect(page).toHaveURL(/team/i);
    });

    test('non staff user accessing /host/1234/score redirects to team', async ({ page }) => {
        await page.goto('/host/1234/score');
        await expect(page).toHaveURL(/team/i);
    });

    test('non staff user accessing /host/1234/leaderboard redirects to team', async ({ page }) => {
        await page.goto('/host/1234/leaderboard');
        await expect(page).toHaveURL(/team/i);
    });
});

test.describe('logged in users cannot access login routes', async () => {
    test.beforeEach(async ({ page }) => {
        await login(page);
    });

    test('logged in user is redirect to /team when trying to go to /user/login', async ({ page }) => {
        await expect(page).toHaveURL(/team/i);
        await page.goto('/user/login');
        await expect(page).toHaveURL(/team/i);
    });

    test('logged in user is redirect to /team when trying to go to /', async ({ page }) => {
        await expect(page).toHaveURL(/team/i);
        await page.goto('/');
        await expect(page).toHaveURL(/team/i);
    });

    // TODO: this is a legit fail and the code around it needs to be fixed
    test.skip('/team with a next query param redirects to next', async ({ page }) => {
        await page.goto('/team?next=game/1234');
        await page.selectOption('select#team-select', { label: playerSelectedTeam });
        await page.locator('text=Choose This Team').click();

        await expect(page).toHaveURL('/game/1234');
    });
});

test.describe('tests for a player without an active team', async () => {
    test.beforeEach(async ({ page }) => {
        await login(page, { username: 'sample_admin', password: 'sample_admin' });
    });

    test('user with no active team is redirected to /team when trying to join a trivia event', async ({ page }) => {
        await page.goto('/game/1234');
        await expect(page).toHaveURL(/team/i);
    });

    test('user with no active team is redirected to /team when trying to access a leaderboard', async ({ page }) => {
        await page.goto('/game/1234/leaderboard');
        await expect(page).toHaveURL(/team/i);
    });

    test('user with no active team is redirected to /team when trying to access a megaround', async ({ page }) => {
        await page.goto('/game/1234/megaround');
        await expect(page).toHaveURL(/team/i);
    });

    test('user with no active team is redirected to /team when trying to access team chat', async ({ page }) => {
        await page.goto('/game/1234/chat');
        await expect(page).toHaveURL(/team/i);
    });
});

// TODO:
// test expired (or lack of) jwt when connectiong to websocket
// - should be logged out and endup back at login
