import { expect, test } from './authfixture.spec.js';

test('log in and go to root', async ({ authPage }) => {
    const page = authPage.page;
    await page.goto('/');

    await expect(page).toHaveTitle(/Host Choice/);
});