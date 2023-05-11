import { expect, request } from '@playwright/test';
import type { Browser, Cookie, Page } from '@playwright/test';

const api_port = process.env.API_PORT || '7000';

/**
 * test refator ideas:
 * use repeatable authentication (file based creds with storageState)
 * - https://playwright.dev/docs/auth#multiple-signed-in-roles
 * integrate that with POM classes
 * - https://playwright.dev/docs/auth#testing-multiple-roles-with-pom-fixtures
 * consider running tests in bigger files in parallel
 * - https://playwright.dev/docs/test-parallel
 * must figure out a better data reset system
 * must use data that won't be modified by users (i.e. don't user event 1234)
 * must reduce configurations (i.e. vscode tasks, playwright configs, npm tasks)
 */

export interface TestConfig {
    username?: string;
    password?: string;
    pageUrl?: string;
    destinationUrl?: string;
    joincode?: string;
    cookies?: Cookie[];
    authStoragePath?: string;
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
    await page.locator('button', { hasText: 'Submit' }).click();
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

export async function asyncTimeout(ms = 100): Promise<ReturnType<typeof setTimeout>> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Return a Page object from the Browser context
 * @param browser
 * @returns page
 */
export const getBrowserPage = async (browser: Browser): Promise<Page> => {
    return browser.newContext().then((context) => context.newPage());
};

export const resetEventData = async (body: Record<string, unknown> = {}) => {
    const context = await request.newContext({
        baseURL: `http://localhost:${api_port}`
    });
    const response = await context.post('/reset-event-data', {
        headers: { 'content-type': 'application/json', accept: 'application/json' },
        data: { secret: 'todd is great', ...body }
    });
    expect(response.status()).toBe(200);
    context.dispose();
};
