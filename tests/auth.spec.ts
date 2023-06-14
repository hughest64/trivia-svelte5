import { expect, test } from './authConfigs.js';
import { createApiContext, login } from './utils.js';
import type { APIRequestContext } from '@playwright/test';

const joincode = '9906';

const game_data = {
    joincode,
    player_limit: true
};

let apicontext: APIRequestContext;

test.beforeAll(async ({ host }) => {
    apicontext = await createApiContext();
    const resp = await apicontext.post('/ops/run-game/', {
        headers: await host.getAuthHeader(),
        data: { game_data: JSON.stringify(game_data) }
    });
    expect(resp.status()).toBe(200);
});

test.afterAll(async () => {
    await apicontext.dispose();
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

test('navigate to a game', async ({ p3 }) => {
    await p3.page.goto('/team');
    await expect(p3.page).toHaveTitle(/team/i);
    const submitBtn = p3.page.locator('button#team-select-submit');
    await expect(submitBtn).toBeVisible();
    await submitBtn.click();
    await expect(p3.page).toHaveURL(/\/game\/join/);
    await expect(p3.page).toHaveTitle(/join/i);
    expect(await p3.page.textContent('h1')).toBe('Enter Game Code');
    // TODO: not 1234
    await p3.page.locator('input[name="joincode"]').fill(joincode);
    await p3.page.locator('text=Join Game!').click();
    await expect(p3.page).toHaveTitle(/event \d+/i);
});

test('logout navigates back to the home page', async ({ p4 }) => {
    await p4.page.goto('/team');
    await p4.page.locator('text=menu').click();
    await p4.page.locator('text=Logout').click();
    await expect(p4.page).toHaveURL('/');
});

// host navigates to a game
test('host navigation options', async ({ host }) => {
    // hosts can play
    await host.page.goto('/host/choice');
    await expect(host.page).toHaveTitle(/host or play/i);
    await host.page.locator('text=Play Trivia').click();
    await expect(host.page).toHaveTitle(/team/i);

    // host can host
    await host.page.goBack();
    await expect(host.page).toHaveTitle(/host or play/i);
    await host.page.locator('text=Host a Game').click();
    await expect(host.page).toHaveURL(/\/host\/event-setup/);
});

test('navigate directly to a game', async ({ p2 }) => {
    await p2.page.goto('/game/9906');
    // expect the message to appear
    const linkText = p2.page.locator('button', { hasText: 'Click here' });
    await expect(linkText).toBeVisible();
    // expect the anwer input to be disabled
    await expect(p2.responseInput).toBeDisabled();
    // click the link
    await linkText.click();
    // expect the answer input to be editable
    await expect(p2.responseInput).toBeEditable();
    // expect the message to go away
    await expect(linkText).not.toBeVisible();
});

test('two players cannot join an event with a player limit', async ({ p3, p4 }) => {
    await p3.joinGame(joincode);
    await p4.joinGame(joincode);

    // should still be on /game/join but with error text
    await expect(p4.page).toHaveURL(/\/game\/join/);
    await expect(p4.page.locator('p.error', { hasText: /already joined/i })).toBeVisible();
    // direct navigate
    await p4.page.goto('/game/9906');
    // should be on error page
    await expect(p4.page.locator('p', { hasText: /player limit/i })).toBeVisible();
    // click join a different game
    await p4.page.locator('a', { hasText: /different game/i }).click();
    // should be on /game/join
    await expect(p4.page).toHaveURL('/game/join');
    // click back
    await p4.page.goBack();
    // click select a different team
    await p4.page.locator('a', { hasText: /different team/i }).click();
    // should b on /team
    await expect(p4.page).toHaveURL('/team');
});

test.describe('user creation', async () => {
    test.beforeEach(async ({ host }) => {
        apicontext.post('ops/delete/', {
            headers: await host.getAuthHeader(),
            data: { type: 'user', usernames: ['testuser'] }
        });
    });

    // TODO delete the user when done
    test('correct handling of user creation', async ({ page }) => {
        const pass1 = 'abc123';
        const pass2 = 'abd345';

        await page.goto('/user/login');

        const usernameField = page.locator('input[name="username"]');

        const pass1Field = page.locator('input[name="pass"]');
        const pass2Field = page.locator('input[name="pass2"]');
        const emailField = page.locator('input[name="email"]');
        const submitButton = page.locator('button', { hasText: /sign up/i });

        // // user should not exist
        await login(page, { username: 'testuser', password: pass1 });
        await expect(page.locator('h3', { hasText: /invalid/i })).toBeVisible();

        // or / and click login then click create account
        await page.goto('/user/create');
        // fill in the form w/ a username that already exists
        await usernameField.fill('player');
        await pass1Field.fill(pass1);
        await pass2Field.fill(pass1);
        await emailField.fill('testuser@no.no');
        await submitButton.click();
        await expect(page).toHaveURL('/user/create');
        await expect(page.locator('p.error')).toHaveText(/already exists/i);

        // update the username but use an exisiting email
        await usernameField.fill('testuser');
        await pass1Field.fill(pass1);
        await pass2Field.fill(pass1);
        await emailField.fill('no@no.no');
        await submitButton.click();
        await expect(page).toHaveURL('/user/create');
        await expect(page.locator('p.error')).toHaveText(/already exists/i);

        // fill in the form w/ passwords that don't match
        await usernameField.fill('testuser');
        await pass1Field.fill(pass1);
        await pass2Field.fill(pass2);
        await emailField.fill('testuser@no.no');
        await submitButton.click();
        await expect(page).toHaveURL('/user/create');
        await expect(page.locator('p.error')).toHaveText(/passwords do not match/i);

        // fill in the form correctly
        await usernameField.fill('testuser');
        await pass1Field.fill(pass1);
        await pass2Field.fill(pass1);
        await emailField.fill('testuser@no.no');
        await submitButton.click();

        await expect(page).toHaveURL('/team');
    });
});
