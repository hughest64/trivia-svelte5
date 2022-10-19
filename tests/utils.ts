import { expect } from '@playwright/test';
import type { Page } from '@playwright/test';

export interface TestConfig {
    username?: string;
    password?: string;
    pageUrl?: string;
    destinationUrl?: string;
}

export const defaultTestConfig: TestConfig = {
    username: 'player',
    password: 'player',
    pageUrl: '/user/login'
};

export const login = async (page: Page, config: TestConfig = {}): Promise<void> => {
    const { pageUrl, username, password }: TestConfig = { ...defaultTestConfig, ...config };

    if (pageUrl) await page.goto(pageUrl);
    await page.locator('input[name="username"]').fill(username as string);
    await page.locator('input[name="password"]').fill(password as string);
    await page.locator('input[value="Submit"]').click();
};

export const authRedirects = async (page: Page, config: TestConfig = {}) => {
    const { pageUrl, username, password, destinationUrl }: TestConfig = { ...defaultTestConfig, ...config };
    // expect to land on a destination url if proived otherwise the original page url
    const endpoint = destinationUrl || pageUrl;

    await page.goto(pageUrl as string);
    await expect(page).toHaveTitle(/welcome/i);

    await page.locator('text=Login/Create Account').click();
    await expect(page).toHaveTitle(/login/i);
    expect(await page.textContent('h1')).toBe('Login');

    await login(page, { username, password, pageUrl: '' });
    await expect(page).toHaveURL(endpoint as string);
};

export const createSelectorPromises = (page: Page, visibleLinks: string[], footerLinks: string[]): Promise<void>[] => {
    const linkPromises = footerLinks.map((link: string) => {
        const selector = expect(page.locator(`p:has-text("${link}")`));
        return visibleLinks.includes(link) ? selector.toBeVisible() : selector.not.toBeVisible();
    });

    return linkPromises;
};
