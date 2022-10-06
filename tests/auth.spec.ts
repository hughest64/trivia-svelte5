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

test.describe('navigate to a trivia event as player', async () => {
    let page: Page;
    test.beforeAll(async ({ browser }) => {
        page = await browser.newPage();
        await login(page);
    });
    test.afterAll(async () =>  await page.close());

    // select a team
    test('select a team then navigate', async () => {
        await expect(page).toHaveTitle(/team/i);
        expect (await page.textContent('h1')).toBe('Create a New Team');

        // check the select options to make sure there is at least one option
        // TODO: validate this works properly
        await page.selectOption('select#team-select', { label: 'hello world' });
        // await page.locator('input[name="selectedteam"]').isVisible();

        await page.locator('text=Choose This Team').click();
    });

    test('enter a join code then navigate', async () => {
        await expect(page).toHaveTitle(/join/i);
        expect(await page.textContent('h1')).toBe('Enter Game Code');
        // TODO: the regex here might be flaky, rethink this test
        // maybe :has-text? https://playwright.dev/docs/selectors
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

test.describe('navigate to trivia event as host', async () => {
    let page: Page;
    test.beforeAll(async ({ browser }) => {
        page = await browser.newPage();
        await login(page, 'sample_admin', 'sample_admin');
    });
    test.afterAll(async () =>  {
        await page.goto('/user/logout');
        await page.close();
    });

    // test click 'Play Trivia
    // expect to be on team select

    // test hit the back button
    // expect to be on /host/choice

    test('host choice is visible', async () => {
        await expect(page).toHaveTitle(/host or play/i);
        expect(await page.textContent('h1')).toBe('Greetings sample_admin');
        await page.locator('text=Host a Game').click();
    });
    // test('event setup')
    // test('event page')
});

// TODO: host side tests
// host side redirect and login to specific endpoints
// host/event-setup
// host/1234
// test non-staff redirects too?

// TODO: we need to determine the desired behavior here!
// - navigate to login when already logged in (as player and host)
