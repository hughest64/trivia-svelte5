import { expect, request } from '@playwright/test';
import type { Cookie, Locator, Page } from '@playwright/test';

export const api_port = process.env.API_PORT || '7000';

export interface TestConfig {
    username?: string;
    password?: string;
    teamName?: string;
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

export interface LbEntryConfig {
    name: RegExp | string;
    rank: RegExp | string;
    points: RegExp | string;
}

export const checkLbEntry = async (entry: Locator, config: LbEntryConfig) => {
    const { name, rank, points } = config;
    await expect(entry.locator('h3.team-name-display')).toHaveText(name);
    await expect(entry.locator('h3.rank-display')).toHaveText(rank);
    await expect(entry.locator('h3.points-display')).toHaveText(points);
};

export const createApiContext = async () => {
    return await request.newContext({
        baseURL: `http://localhost:${api_port}`,
        extraHTTPHeaders: { 'content-type': 'application/json', accept: 'application/json' }
    });
};
