import { expect, test } from '@playwright/test';
import type { Page } from '@playwright/test';
import { authRedirects, login } from './utils.js';

test('guest login', async ({ page }) => {
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

test.describe('navigate to a trivia event', async () => {
    let page: Page;
    test.beforeAll(async ({ browser }) => {
        page = await browser.newPage();
        await login(page);
    });
    test.afterAll(async () => {
        await page.close();
    });

    // select a team
    test('select a team then navigate', async () => {
        await expect(page).toHaveTitle(/team/i);
        expect (await page.textContent('h1')).toBe('Create a New Team');

        // check the select options to make sure there is at least one option
        await page.selectOption('select#team-select', { label: 'hello world' });
        // await page.locator('input[name="selectedteam"]').isVisible();

        await page.locator('text=Choose This Team').click();
    });

    test('enter a join code then navigate', async () => {
        await expect(page).toHaveTitle(/join/i);
        expect(await page.textContent('h1')).toBe('Enter Game Code');
        expect(await page.textContent('p')).not.toBe(/undefined/i);
        
        await page.locator('input[name="joincode"]').fill('1234');
        await page.locator('text=Join Game!').click();
    });

    test('navigate to trivia event', async () => {
        // the join code should be in the title (good enough for now)
        await expect(page).toHaveTitle(/event 1234/i);
    });

    test('logout navigates back to the home page', async () => {
        await page.locator('text=menu').click();
        await page.locator('text=Logout').click();
        await expect(page).toHaveURL('/');
    });
});

// TODO: host side tests
// host side redirect and login to specific endpoints
// host/event-setup
// host/1234
// test non-staff redirects too?
// test hook similar plaher side for host (i.e. route all the way from login to hosting an event)

// TODO: we need to determine the desired behavior here!
// - navigate to login when already logged in (as player and host)
