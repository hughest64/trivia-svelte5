import { expect, test } from '@playwright/test';
import { authRedirects, getBrowserPage, login, resetEventData } from './utils.js';
import { PlayerGamePage } from './gamePages.js';
import type { Page } from '@playwright/test';

const adminUser = 'sample_admin';
const playerSelectedTeam = 'hello world';

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

// redirects to specific endpoints
test('proper redirect for game home page', async ({ page }) => authRedirects(page, { pageUrl: '/team' }));
test('proper redirect for game join page', async ({ page }) => authRedirects(page, { pageUrl: '/game/join' }));
test('proper redirect for game page', async ({ page }) => authRedirects(page, { pageUrl: '/game/1234' }));
test('proper redirect for host choice page', async ({ page }) =>
    authRedirects(page, { username: adminUser, password: adminUser, pageUrl: '/host/choice' }));
test('proper redirect for host event setup', async ({ page }) =>
    authRedirects(page, { username: adminUser, password: adminUser, pageUrl: '/host/event-setup' }));
test('proper redirect for host game page', async ({ page }) =>
    authRedirects(page, { username: adminUser, password: adminUser, pageUrl: '/host/1234' }));

test.describe('navigate to a trivia event as player', async () => {
    let page: Page;
    test.beforeAll(async ({ browser }) => {
        page = await browser.newPage();
        await login(page);
    });
    test.afterAll(async () => await page.close());

    // select a team
    test('select a team then navigate', async () => {
        await expect(page).toHaveTitle(/team/i);
        expect(await page.textContent('h1')).toBe('Create a New Team');
        await page.selectOption('select#team-select', { label: playerSelectedTeam });
        await page.locator('text=Choose This Team').click();
    });

    test('active team name is displayed on the join page', async () => {
        await expect(page).toHaveTitle(/join/i);
        expect(await page.textContent('h1')).toBe('Enter Game Code');
        await expect(page.locator(`p:has-text("${playerSelectedTeam}")`)).toBeVisible();
    });

    test('navigate to trivia event', async () => {
        await page.locator('input[name="joincode"]').fill('1234');
        await page.locator('text=Join Game!').click();
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
        await login(page, { username: adminUser, password: adminUser });
    });
    test.afterAll(async () => {
        await page.goto('/user/logout');
        await page.close();
    });

    test('host can be a player', async () => {
        await expect(page).toHaveTitle(/host or play/i);
        await page.locator('text=Play Trivia').click();
        await expect(page).toHaveTitle(/team/i);
    });

    test('the back button navigates to host choice', async () => {
        await page.goBack();
        await expect(page).toHaveTitle(/host or play/i);
    });

    test('host choice is visible', async () => {
        await expect(page).toHaveTitle(/host or play/i);
        expect(await page.textContent('h1')).toBe(`Greetings ${adminUser}`);
        await page.locator('text=Host a Game').click();
    });

    test('event setup has event options', async () => {
        await expect(page).toHaveURL('/host/event-setup');
        expect(await page.textContent('h1')).toBe('Choose a Trivia Event');

        // TODO: test the select menus for content

        await page.locator('button:has-text("Begin Event")').click();
        await expect(page).toHaveURL(/\/host\/\d+\/?$/i);
    });
});

test('navigate directly to a game', async ({ browser }) => {
    const p1 = new PlayerGamePage(await getBrowserPage(browser), { pageUrl: '/game/1234' });
    p1.login();
    // expect the message to appear
    const linkText = p1.page.locator('button', { hasText: 'Click here' });
    await expect(linkText).toBeVisible();
    // expect the anwer input to be disabled
    await expect(p1.responseInput).toBeDisabled();
    // click the link
    await linkText.click();
    // expect the answer input to be editable
    await expect(p1.responseInput).toBeEditable();
    // expect the message to go away
    await expect(linkText).not.toBeVisible();

    await resetEventData();
});
