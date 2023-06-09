import * as fs from 'fs';
import { expect, test as base } from '@playwright/test';
import { PlayerGamePage, HostGamePage } from './gamePages.js';
import type { Browser, Cookie } from '@playwright/test';
import type { TestConfig } from './utils.js';

export type UserAuthConfigs = Record<
    string,
    Pick<TestConfig, 'username' | 'password' | 'authStoragePath' | 'cookies' | 'teamName'>
>;

export interface AuthFixtures {
    p1: PlayerGamePage;
    p2: PlayerGamePage;
    p3: PlayerGamePage;
    p4: PlayerGamePage;
    host: HostGamePage;
}

export const userAuthConfigs: UserAuthConfigs = {
    playerOne: {
        username: 'player',
        password: 'player',
        teamName: 'hello world',
        authStoragePath: 'playwright/.auth/player.json'
    },
    playerTwo: {
        username: 'player_two',
        password: 'player_two',
        teamName: 'hello world',
        authStoragePath: 'playwright/.auth/playertwo.json'
    },
    playerThree: {
        username: 'player_three',
        password: 'player_three',
        teamName: 'for all the marbles',
        authStoragePath: 'playwright/.auth/playerthree.json'
    },
    playerFour: {
        username: 'player_four',
        password: 'player_four',
        teamName: 'for all the marbles',
        authStoragePath: 'playwright/.auth/playerfour.json'
    },
    host: {
        username: 'sample_admin',
        password: 'sample_admin',
        authStoragePath: 'playwright/.auth/host.json'
    }
};

export const getUserPage = async (browser: Browser, userId: string) => {
    const config = userAuthConfigs[userId];
    if (config === undefined) {
        throw new Error(`no configuration was found for userId ${userId}`);
    }
    const storagePath = config.authStoragePath || '';
    if (storagePath && !fs.existsSync(storagePath)) {
        fs.writeFileSync(storagePath, JSON.stringify({}));
    } else {
        const cookieData: Cookie[] = JSON.parse(fs.readFileSync(storagePath).toString()).cookies || [];
        const jwtExp = Math.round(cookieData.find((cookie) => cookie.name === 'jwt')?.expires || 0) * 1000;

        // reset the file if the token is expired
        if (Date.now() > jwtExp) {
            console.log(`resetting auth for ${userId}`);
            fs.writeFileSync(storagePath, JSON.stringify({}));
        }
    }

    const context = await browser.newContext({ storageState: config.authStoragePath });
    const page = await context.newPage();
    config.cookies = await context.cookies();

    const userPage = userId === 'host' ? new HostGamePage(page, config) : new PlayerGamePage(page, config);
    await userPage.useAuthConfig();

    return userPage;
};

export const test = base.extend<AuthFixtures>({
    p1: async ({ browser }, use) => {
        const pg = (await getUserPage(browser, 'playerOne')) as PlayerGamePage;
        await use(pg);
        await pg.page.context().close();
    },
    p2: async ({ browser }, use) => {
        const pg = (await getUserPage(browser, 'playerTwo')) as PlayerGamePage;
        await use(pg);
        await pg.page.context().close();
    },
    p3: async ({ browser }, use) => {
        const pg = (await getUserPage(browser, 'playerThree')) as PlayerGamePage;
        await use(pg);
        await pg.page.context().close();
    },
    p4: async ({ browser }, use) => {
        const pg = (await getUserPage(browser, 'playerFour')) as PlayerGamePage;
        await use(pg);
        await pg.page.context().close();
    },
    host: async ({ browser }, use) => {
        const pg = (await getUserPage(browser, 'host')) as HostGamePage;
        await use(pg);
        await pg.page.context().close();
    }
});

// alias expect so we can import test an expect from the same file
export { expect };
