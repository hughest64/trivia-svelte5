import { expect } from '@playwright/test';
import type { Page } from '@playwright/test';

export const defaultCredentials = {
    username: 'player',
    password: 'player'
};

// TODO: config objects for all params except page
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

// TODO: pageUrl/username/password should be a "config" object along with expected endpoint
// if that is empty, it can be set to the desired endpoint, i.e.
// const expectdEndpoint = config.expectedEndpoint || config.desiredEncpoint
export const authRedirects = async (
    page: Page,
    pageUrl: string,
    username = defaultCredentials.username,
    password = defaultCredentials.password
) => {
    await page.goto(pageUrl);
    await expect(page).toHaveTitle(/welcome/i);

    await page.locator('text=Login/Create Account').click();
    await expect(page).toHaveTitle(/login/i);
    expect(await page.textContent('h1')).toBe('Login');

    await login(page, username, password, '');
    await expect(page).toHaveURL(pageUrl);
};

export const createSelectorPromises = (page: Page, visibleLinks: string[], footerLinks: string[]): Promise<void>[] => {
    const linkPromises = footerLinks.map((link: string) => {
        const selector = expect(page.locator(`p:has-text("${link}")`));
        return visibleLinks.includes(link) ? selector.toBeVisible() : selector.not.toBeVisible();
    });

    return linkPromises;
};
