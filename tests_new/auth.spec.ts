import { expect, test } from '@playwright/test';
import { createApiContext, login, getUserPage, userAuthConfigs } from './config.js';
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

test('login as host', async ({ page }) => {
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

test('login as player', async ({ page }) => {
    const user = userAuthConfigs.player_four;
    const activeTeam = (user.team_names || [])[0];
    await page.goto('/user/login');
    await login(page, user.username, user.password, false);
    await expect(page).toHaveURL('/team');
    // check that team is selected
    const teamSelect = page.locator('option', { hasText: activeTeam });
    await expect(teamSelect).toHaveText(activeTeam);

    // click let's play
    await page.locator('button', { hasText: /let's play/i }).click({ timeout: 5000 });
    // should be on the join page w/ team name visible
    await expect(page).toHaveURL('/game/join');
    // we can see the user's active team
    await expect(page.locator('h2', { hasText: activeTeam })).toBeVisible();
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
