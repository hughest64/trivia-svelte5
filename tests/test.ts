import { expect, test } from '@playwright/test';

import * as cookie from 'cookie';

// TODO: event adding tests to tsconfig, tests won't run cuz it can't import this
// maybe fixed for 1.0? https://github.com/sveltejs/kit/issues/5833
// import { setCsrfHeaders } from '$lib/utils';

/**
 * TODO:
 * run the tests on port 3010 (or just not 3000 so the we can run the app at the same time)
 * maybe we should hit a test server on the api?
 * it would be nice to configure auto starting the Django side (with test server?)
 * when tests are run.
 */

// TODO: fixture - once you are logged in, store the creds (however we do that)
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

// test team select (list of teams) and navigation to game-select - perhaps this should not be present for guest?
// test team select (team password) and navigation to game-select
// - good password,
// - bad password
// test team creation and navigation to game-select
// test joining a game as a guest
// test logging out

test('login page redirects properly', async ({ page }) => {
    // TODO: we need to extract this for authentication all over,
    // we need to always hit /user/login/ first as that's the only place to get the token
    const resp = await page.goto('/user/login');
    const headers = (await resp?.allHeaders()) || {};
    const cookies = headers['set-cookie'];
    const csrfToken = (cookies && cookie.parse(cookies).csrftoken) || '';

    // TODO: we probably don't need to cet the X-CSRF in the app!
    await page.setExtraHTTPHeaders({ Cookie: `csrftoken=${csrfToken}` });

    // BROKEN!
    // await page.setExtraHTTPHeaders(setCsrfHeaders(csrfToken));

    expect(await page.textContent('h1')).toBe('Login');

    await page.locator('input[name="username"]').fill('sample_admin');
    await page.locator('input[name="password"]').fill('sample_admin');
    await page.locator('input[type="submit"]').click();

    await expect(page).toHaveTitle(/Host Choice/);
    expect(await page.textContent('h1')).toBe('Greetings sample_admin');
});
