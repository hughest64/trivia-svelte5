import { expect, test } from '@playwright/test';
import type { Cookie } from '@playwright/test';

// TODO: new fixture overriding page as outlined below
test('unauthenticated request to /game/join redirects properly', async ({ page }) => {

    // TODO: make this a paramerter passed to test
    await page.goto('/game/join');
    await expect(page).toHaveTitle(/welcome/i);
    
    await page.locator('text=Login/Create Account').click();
    expect(await page.textContent('h1')).toBe('Login');

    const cookies = await page.context().cookies();
    const csrfToken = <Cookie | undefined>cookies.find((cookie) => cookie.name === 'csrftoken');
    csrfToken && await page.setExtraHTTPHeaders({
        Cookie: `csrftoken=${csrfToken?.value || ''}`,
        'X-CSRFToken': csrfToken?.value || ''
    });

    // TODO: use guest instead of sample_admin, but perhaps user info could be a parameter?
    await page.locator('input[name="username"]').fill('sample_admin');
    await page.locator('input[name="password"]').fill('sample_admin');
    await page.locator('input[value="Submit"]').click();
    
    // TODO: not part of the fixture as the critera changes per page
    await expect(page).toHaveTitle(/join/i);
    expect(await page.textContent('h1')).toBe('Enter Game Code');
});
