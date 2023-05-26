import * as fs from 'fs';
import { PlayerGamePage, HostGamePage } from './gamePages.js';
import type { Browser, Cookie } from '@playwright/test';
import type { TestConfig } from './utils.js';

export type UserAuthConfigs = Record<string, Pick<TestConfig, 'username' | 'password' | 'authStoragePath' | 'cookies'>>;

export const userAuthConfigs: UserAuthConfigs = {
    playerOne: {
        username: 'player',
        password: 'player',
        authStoragePath: 'playwright/.auth/player.json'
    },
    playerTwo: {
        username: 'player_two',
        password: 'player_two',
        authStoragePath: 'playwright/.auth/playertwo.json'
    },
    playerThree: {
        username: 'player_three',
        password: 'player_three',
        authStoragePath: 'playwright/.auth/playerthree.json'
    },
    playerFour: {
        username: 'player_four',
        password: 'player_four',
        authStoragePath: 'playwright/.auth/playerfour.json'
    },
    host: {
        username: 'sample_admin',
        password: 'sample_admin',
        authStoragePath: 'playwright/.auth/host.json'
    },
    run_game_user_1: {
        username: 'run_game_user_1',
        password: '12345',
        authStoragePath: 'playwright/.auth/some_user.json'
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
