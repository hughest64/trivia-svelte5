import type { Cookie, Browser, Page } from '@playwright/test';
import { PlayerGamePage, HostGamePage } from './gamePages.js';
import type { TestConfig } from './utils.js';

export interface PageContextData {
    userCookies: Cookie[];
    page: Page;
}

export type UserAuthConfigs = Record<string, Pick<TestConfig, 'username' | 'password' | 'authStoragePath' | 'cookies'>>;

export type GetFromContextTypes = (browser: Browser, storagePath: string) => Promise<PageContextData>;

export const getPageFromContext: GetFromContextTypes = async (browser, storagePath) => {
    const context = await browser.newContext({ storageState: storagePath });
    const userCookies = await context.cookies();
    const page = await context.newPage();

    return { userCookies, page };
};

export const userAuthConfigs: UserAuthConfigs = {
    playerOne: {
        username: 'player',
        password: 'player',
        authStoragePath: 'playwright/.auth/player.json'
    },
    playerTwo: {
        username: 'player_two',
        password: 'player_two',
        authStoragePath: 'playwright/.auth/player.json'
    },
    playerThree: {
        username: 'player_three',
        password: 'player_three',
        authStoragePath: 'playwright/.auth/player.json'
    },
    playerFour: {
        username: 'player_four',
        password: 'player_four',
        authStoragePath: 'playwright/.auth/player.json'
    },
    host: {
        username: 'sample_admin',
        password: 'sample_admin',
        authStoragePath: 'playwright/.auth/player.json'
    },
    run_game_user_1: {
        username: 'run_game_user_1',
        password: '12345',
        authStoragePath: 'playwright/.auth/some_user.json'
    }
};

// TODO: key of UserAuthConfig?
export const getUserPage = async (browser: Browser, userId: string) => {
    const config = userAuthConfigs[userId];
    if (config === undefined) {
        throw new Error(`no configuration was found for userId ${userId}`);
    }
    const { page, userCookies } = await getPageFromContext(browser, config.authStoragePath as string);
    config.cookies = userCookies;
    let userPage: PlayerGamePage | HostGamePage;
    if (userId === 'host') {
        userPage = new HostGamePage(page, config);
    } else {
        userPage = new PlayerGamePage(page, config);
    }
    await userPage.useAuthConfig();

    return userPage;
};
