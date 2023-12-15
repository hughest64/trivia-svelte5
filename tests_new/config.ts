import * as fs from 'fs';

import { request } from '@playwright/test';
import games from '../tests/data/games.json' assert { type: 'json' };
import users from '../tests/data/users.json' assert { type: 'json' };
import type { Browser, Cookie, Page } from '@playwright/test';

export const api_port = process.env.API_PORT || '7000';
export interface UserAuthConfig {
    username: string;
    password: string;
    email: string;
    team_name?: string;
    is_staff?: boolean;
    auth_storage_path: string;
    cookies?: Cookie[];
}

// automatcially use the keys defined in the users object
type UserKey = keyof typeof users;
export const userAuthConfigs: Record<UserKey, UserAuthConfig> = users;

export const login = async (page: Page, username: string, password: string, navigate = true) => {
    navigate && (await page.goto('/user/login'));
    await page.locator('input[name="username"]').fill(username);
    await page.locator('input[name="password"]').fill(password);
    await page.locator('button[type="submit"]').click({ timeout: 5000 });
};

export const logout = async (page: Page) => {
    await page.goto('/user/logout');
};

export type AuthHeaders = Record<'Cookie' | 'X-CSRFToken', string>;
export const getAuthHeaders = async (page: Page): Promise<AuthHeaders> => {
    const cookies = await page.context().cookies();
    const csrftoken = cookies.find((c) => c.name === 'csrftoken')?.value || '';
    const jwt = cookies.find((c) => c.name === 'jwt')?.value || '';
    const headers = {
        Cookie: `jwt=${jwt};csrftoken=${csrftoken}`,
        'X-CSRFToken': csrftoken
    };
    return headers;
};

export const createApiContext = async (page: Page) => {
    const authHeaders = await getAuthHeaders(page);

    return request.newContext({
        baseURL: `http://127.0.0.1:${api_port}`,
        extraHTTPHeaders: { 'content-type': 'application/json', accept: 'application/json', ...authHeaders }
    });
};

export const getUserPage = async (browser: Browser, userId: UserKey): Promise<Page> => {
    const config = userAuthConfigs[userId];
    if (config === undefined) {
        throw new Error(`no configuration was found for userId ${userId}`);
    }
    const storagePath = config.auth_storage_path;
    let expired = false;
    try {
        // check if the token is valid
        const cookieData: Cookie[] = JSON.parse(fs.readFileSync(storagePath).toString()).cookies || [];
        const jwtExp = Math.round(cookieData.find((cookie) => cookie.name === 'jwt')?.expires || 0) * 1000;
        if (Date.now() > jwtExp) expired = true;
    } catch {
        // create an auth file if it doesn't exist
        fs.writeFileSync(storagePath, JSON.stringify({}));
        expired = true;
    }

    const context = await browser.newContext({ storageState: config.auth_storage_path });
    const page = await context.newPage();
    // reset the file if the token is expired
    if (expired) {
        console.log(`resetting auth for ${userId}`);
        // TODO: can we hook into the api directly instead of logging in via browser?
        await login(page, config.username, config.password);
        await page.context().storageState({ path: config.auth_storage_path });
    }
    config.cookies = await context.cookies();

    return page;
};

export async function asyncTimeout(ms = 100): Promise<ReturnType<typeof setTimeout>> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

export { games };
