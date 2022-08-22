import { expect } from '@playwright/test';
import type { Page } from '@playwright/test';

export const authRedirects = async (page: Page, pageUrl: string) => {
    await page.goto(pageUrl);
    await expect(page).toHaveTitle(/welcome/i);
    
    await page.locator('text=Login/Create Account').click();
    await expect(page).toHaveTitle(/login/i);
    expect(await page.textContent('h1')).toBe('Login');

    // TODO: use guest instead of sample_admin, but perhaps user info could be a parameter?
    await page.locator('input[name="username"]').fill('sample_admin');
    await page.locator('input[name="password"]').fill('sample_admin');
    await page.locator('input[value="Submit"]').click();

    await expect(page).toHaveURL(pageUrl);

};


// TODO: not part of the fixture as the critera changes per page - use for separate log in tests!
// await expect(page).toHaveTitle(/join/i);
// expect(await page.textContent('h1')).toBe('Enter Game Code');

// await page.locator('input[name="joincode"]').fill('1234');
// await page.locator('input[value="Join Game!"]').click();

// await expect(page).toHaveTitle(/event 1234/i);