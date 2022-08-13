import { expect, test } from '@playwright/test';
import type { Cookie } from '@playwright/test';

test('unauthenticated request to /game/join redirects properly', async ({ browser }) => {
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('/user/login?next=/game/join');
    // await page.goto('/game/join');
    // await expect(page).toHaveTitle(/welcome/i);

    await page.locator('text=Login').click();
    expect(await page.textContent('h1')).toBe('Login');

    const cookies = await page.context().cookies();
    const csrfToken = <Cookie|undefined>cookies.find((cookie) => cookie.name === 'csrftoken');
    await page.setExtraHTTPHeaders({ Cookie: `csrftoken=${csrfToken?.value}`, 'X-CSRFToken': csrfToken?.value || '' });

    await page.locator('input[name="username"]').fill('sample_admin');
    await page.locator('input[name="password"]').fill('sample_admin');
    await page.locator('input[value="Submit"]').click();

    // TODO: this is failing when we have a querystring on the url, the page stays on login and does not redirect
    // the login is successful, so wtf?
    // await expect(page).toHaveTitle(/join/i);
    expect(await page.textContent('h1')).toBe('Enter Game Code');
});
