import { expect, test } from '@playwright/test';
import { createApiContext, login, getUserPage } from './config.js';
import type { APIRequestContext, Page } from '@playwright/test';

let apicontext: APIRequestContext;
let apiPage: Page;

test.beforeAll(async ({ browser }) => {
    apiPage = await getUserPage(browser, 'api_user');
    apicontext = await createApiContext(apiPage);
});

test.afterAll(async () => {
    await apiPage.context().close();
    await apicontext.dispose();
});

test('login as host and navigate', async ({ page }) => {
    await page.goto('/user/login');
    await login(page, 'host_user', 'abc123', false);
    await expect(page).toHaveURL('/host/choice');
    await page.locator('text=Play Trivia').click();
    await expect(page).toHaveTitle(/team/i);

    // host can host
    await page.goBack();
    await expect(page).toHaveTitle(/host or play/i);
    await page.locator('text=Host a Game').click();
    await expect(page).toHaveURL(/\/host\/event-setup/);
});

test.skip('login as player and navigate', async ({ page }) => {
    // TODO:
    // implement the resigned flow:
    // - after login should be the joincode page
    // - should be able to navigate elsehwere (/team, user settings, etc) (probably a different test)
    // - enter bad jc
    // - enter good jc
    // -- should show the location of the event and have options to got the game (this does the join)
    //    or enter a new code
});

test.skip('naviagate directly to a game', async ({ page }) => {
    // TODO: decide if the is a
});

test('two players cannot join an event with a player limit', async ({ browser }) => {
    const p1 = getUserPage(browser, 'player_one');
    const p2 = getUserPage(browser, 'player_two');

    // p1 joins game 1111
    // - success
    // p2 (same team) tries to join the game
    // - gets error message - test navigation from the error?
});

test('guest login', async ({ page }) => {
    await page.goto('/');
    // not logged in, we should land on the welcome page
    await expect(page).toHaveTitle(/welcome/i);
    // click to log in as a guest
    await page.locator('text=Play as a Guest').click();
    // since guest is not a staff user, they should see the team select component
    await expect(page).toHaveTitle(/create team/i);
    await expect(page.locator('h2', { hasText: /choose a team name/i })).toBeVisible();
});

const submitCreateForm = async (page: Page, values: Record<string, string>) => {
    const usernameField = page.locator('input[name="username"]');
    await expect(usernameField).toBeVisible();
    await usernameField.fill(values.username);

    const passOneField = page.locator('input[name="pass"]');
    await expect(passOneField).toBeVisible();
    await passOneField.fill(values.passOne);

    const passTwoField = page.locator('input[name="pass2"]');
    await expect(passTwoField).toBeVisible();
    await passTwoField.fill(values.passTwo);

    const emailField = page.locator('input[name="email"]');
    await expect(emailField).toBeVisible();
    await emailField.fill(values.email);

    const submitBtn = page.locator('button[type="submit"]', { hasText: /sign up/i });
    await expect(submitBtn).toBeVisible();
    await submitBtn.click();
};

test('create a user', async ({ page }) => {
    await page.goto('/user/login');
    const createLink = page.locator('a.button', { hasText: /create account/i });
    await expect(createLink).toBeVisible();
    await createLink.click();
    await expect(page).toHaveURL(/\/user\/create/);

    const formValues = {
        username: 'host_user',
        passOne: 'abc123',
        passTwo: 'abc456',
        email: 'no@no.no'
    };

    // mismatched passwords
    await submitCreateForm(page, formValues);
    await expect(page.locator('p.error')).toHaveText(/do not match/i);

    // username exists
    formValues.passTwo = 'abc123';
    await submitCreateForm(page, formValues);
    await expect(page.locator('p.error')).toHaveText(/already exists/i);

    // success!
    formValues.username = 'new_user';
    await submitCreateForm(page, formValues);
    await expect(page).toHaveURL('/team/create');
});

test('reset password', async ({ page }) => {
    // get a reset token from the api
    const resp = await apicontext.post('/user/forgot', {
        data: { username: 'reset_user' }
    });
    expect(resp.status()).toBe(200);
    const respData = await resp.json();
    const token = respData.token;

    // ensure we pick up a csrf token
    await page.goto('/');
    // goto the rest page with the token
    await page.goto(`/user/reset/${token}`);
    await expect(page).toHaveURL(`/user/reset/${token}`);

    // fill in w/ mismatched passwords
    await page.locator('input[name="pass1"]').fill('new_pass', { timeout: 5000 });
    await page.locator('input[name="pass2"]').fill('new_pas', { timeout: 5000 });
    const submitBtn = page.locator('button[type="submit"]');
    await submitBtn.click({ timeout: 5000 });
    await expect(page.locator('p.error')).toHaveText(/passwords do not match/i);

    // matching passwords
    await page.locator('input[name="pass2"]').fill('new_pass', { timeout: 5000 });
    await submitBtn.click({ timeout: 5000 });
    await expect(page).toHaveURL('/team');

    // logout
    await page.goto('/user/logout');
    await expect(page).toHaveURL('/');
    // login w/ new password
    await login(page, 'reset_user', 'new_pass', true);
    await expect(page).toHaveURL('/team/create');
});
