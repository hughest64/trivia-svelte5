import { test as base } from '@playwright/test';
import { authStorage } from './auth.setup.js';
import { PlayerGamePage, HostGamePage } from './gamePages.js';

interface AuthFixtures {
    p1Page: PlayerGamePage;
    p2Page: PlayerGamePage;
    p3Page: PlayerGamePage;
    p4Page: PlayerGamePage;
    hostPage: HostGamePage;
}

// NOTE: there is a bug that causes beforeEach hooks to fail if the value of storageState is not a string literal
export const test = base.extend<AuthFixtures>({
    p1Page: async ({ browser }, use) => {
        const context = await browser.newContext({ storageState: authStorage.playerFile });
        const p1Page = new PlayerGamePage(await context.newPage());
        await use(p1Page);
        await context.close();
    },
    p2Page: async ({ browser }, use) => {
        const context = await browser.newContext({ storageState: authStorage.playerTwoFile });
        const p2Page = new PlayerGamePage(await context.newPage());
        await use(p2Page);
        await context.close();
    },
    p3Page: async ({ browser }, use) => {
        const context = await browser.newContext({ storageState: authStorage.playerThreeFile });
        const p3Page = new PlayerGamePage(await context.newPage());
        await use(p3Page);
        await context.close();
    },
    p4Page: async ({ browser }, use) => {
        const context = await browser.newContext({ storageState: authStorage.playerFourFile });
        const p4Page = new PlayerGamePage(await context.newPage());
        await use(p4Page);
        await context.close();
    },
    hostPage: async ({ browser }, use) => {
        const context = await browser.newContext({ storageState: authStorage.hostFile });
        const hostPage = new HostGamePage(await context.newPage());
        await use(hostPage);
        await context.close();
    }
});

export { expect } from '@playwright/test';
