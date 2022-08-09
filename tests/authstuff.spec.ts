
// @ts-ignore-next-line - ts complains about .ts extentsion, but it's neccessary
// cuz we are useing esm modules (module: true in package.json)
import { expect, test } from './authfixture.spec.ts';

test('log in and go to root', async ({ authPage }) => {
    const page = authPage.page;
    await page.goto('/');

    await expect(page).toHaveTitle(/Host Choice/);
});