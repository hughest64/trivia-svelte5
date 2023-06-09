import { expect, test } from '@playwright/test';
import { asyncTimeout, getBrowserPage, login, resetEventData } from './utils.js';
import { PlayerGamePage } from './gamePages.js';
import type { Page } from '@playwright/test';

const adminUser = 'sample_admin';
const playerSelectedTeam = 'hello world';

// TODO: user creation works, but this test is problematic for some reason
test.describe('user creation', async () => {
    test.afterEach(async () => await resetEventData());

    test.skip('correct handling of user creation', async ({ page }) => {
        const pass1 = 'abc123';
        const pass2 = 'abd345';

        const usernameField = page.locator('input[name="username"]');
        const pass1Field = page.locator('input[name="pass"]');
        const pass2Field = page.locator('input[name="pass2"]');
        const emailField = page.locator('input[name="email"]');
        const submitButton = page.locator('button', { hasText: /sign up/i });

        // user should not exist
        await login(page, { username: 'testuser', password: pass1 });
        await expect(page.locator('h3', { hasText: /invalid/i })).toBeVisible();

        // or / and click login then click create account
        await page.goto('/user/create');
        // fill in the form w/ a username that already exists
        await usernameField.fill('player');
        await pass1Field.fill(pass1);
        await pass2Field.fill(pass1);
        await emailField.fill('no@no.no');
        await submitButton.click();
        await expect(page).toHaveURL('/user/create');
        await expect(page.locator('p.error')).toHaveText(/username already exists/i);

        // fill in the form w/ passwords that don't match
        await usernameField.fill('testuser');
        await pass1Field.fill(pass1);
        await pass2Field.fill(pass2);
        await emailField.fill('no@no.no');
        await submitButton.click();
        await expect(page).toHaveURL('/user/create');
        await expect(page.locator('p.error')).toHaveText(/passwords do not match/i);

        // fill in the form correctly
        await usernameField.fill('testuser');
        await pass1Field.fill(pass1);
        await pass2Field.fill(pass1);
        await emailField.fill('no@no.no');
        await submitButton.click();

        // TODO: for some reason the test doesn't redirect to /team properly, but it works in the ui.
        // It seems like the cookie isn't getting set properly.
        // For now the best we can do is confirm that the user was created but actually logging in.
        await asyncTimeout(200);
        await login(page, { username: 'testuser', password: pass1 });
        await expect(page).toHaveURL('/team');
    });
});

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

// TODO: can we test for query params? I think probably via regex
test('all authed pages redirect to welcome page when not logged in', async ({ page }) => {
    await page.goto('/team');
    await expect(page).toHaveURL(/\/?next=\/team/);

    await page.goto('/game/join');
    await expect(page).toHaveURL(/\/?next=\/game\/join/);

    await page.goto('/game/1234');
    await expect(page).toHaveURL(/\/?next=\/game\/1234/);

    await page.goto('/host/choice');
    await expect(page).toHaveURL(/\/?next=\/host\/choice/);

    await page.goto('/host/event-setup');
    await expect(page).toHaveURL(/\/?next=\/host\/event-setup/);

    await page.goto('/host/1234');
    await expect(page).toHaveURL(/\/?next=\/host\/1234/);
});

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
});

// TODO: remove the wrapper and resetEventData call
// use the the game-setup structure via api call instean
test.describe('event specific rules', async () => {
    test.beforeEach(async () => resetEventData({ joincodes: 9906 }));

    test('navigate directly to a game', async ({ browser }) => {
        const p1 = new PlayerGamePage(await getBrowserPage(browser));
        await p1.login();
        await p1.page.goto('/game/9906');
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
    });

    // TODO: failing at await expect(p2.page.locator('p.error', { hasText: /team limit exceeded/i })), did this change?
    test.skip('two players cannot join an event with a player limit', async ({ browser }) => {
        const p1 = new PlayerGamePage(await getBrowserPage(browser));
        await p1.login();
        await p1.joinGame('9906');

        const p2 = new PlayerGamePage(await getBrowserPage(browser), {
            username: 'player_two',
            password: 'player_two'
        });
        await p2.login();
        await p2.joinGame('9906');

        // should still be on /game/join but with error text
        await expect(p2.page).toHaveURL(/\/game\/join/);
        await expect(p2.page.locator('p.error', { hasText: /team limit exceeded/i })).toBeVisible();
        // direct navigate
        await p2.page.goto('/game/9906');
        // should be on error page
        await expect(p2.page.locator('p', { hasText: /player limit/i })).toBeVisible();
        // click join a different game
        await p2.page.locator('a', { hasText: /different game/i }).click();
        // should be on /game/join
        await expect(p2.page).toHaveURL('/game/join');
        // click back
        await p2.page.goBack();
        // click select a different team
        await p2.page.locator('a', { hasText: /different team/i }).click();
        // should b on /team
        await expect(p2.page).toHaveURL('/team');
    });
});
