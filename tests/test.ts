import { expect, test } from '@playwright/test';

/**
 * TODO:
 * figure out how to check a response code, example:
 * hitting '/' without a valid jwt returns a 403 from the server
 * that redirects to '/user/login' in the app. right now the test
 * just times out because the requested resource never loads (is that right?)
 * 
 * maybe we should hit a test server on the api?
 * it would be nice to configure auto starting the Django side (with test server?)
 * when tests are ran.
 */

test('index page redirects to /user/login when not logged in', async ({ page }) => {
    await page.goto('/user/login');

    expect(await page.textContent('h1')).toBe('Login');
    // expect(true);
});

test('login page has expected h1', async ({ page }) => {
    await page.goto('/user/login/');

    expect(await page.textContent('h1')).toBe('Login');
});
