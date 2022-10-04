import { expect } from '@playwright/test';
import type { Page } from '@playwright/test';

// TODO: use non-staff user not sample_admin
export const defaultCredentials = {
    username: 'player',
    password: 'player'
};

export const login = async (
    page: Page,
    username = defaultCredentials.username,
    password = defaultCredentials.password,
    pageUrl = '/user/login'
): Promise<void> => {
    if (pageUrl) await page.goto(pageUrl);
    await page.locator('input[name="username"]').fill(username);
    await page.locator('input[name="password"]').fill(password);
    await page.locator('input[value="Submit"]').click();
};

export const authRedirects = async (page: Page, pageUrl: string) => {
    await page.goto(pageUrl);
    await expect(page).toHaveTitle(/welcome/i);

    await page.locator('text=Login/Create Account').click();
    await expect(page).toHaveTitle(/login/i);
    expect(await page.textContent('h1')).toBe('Login');

    await login(page, defaultCredentials.username, defaultCredentials.password, '');
    await expect(page).toHaveURL(pageUrl);
};
