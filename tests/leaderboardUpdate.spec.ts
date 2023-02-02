import { expect, test } from '@playwright/test';
import {
    PlayerGamePage
    // HostGamePage
} from './gamePages.js';
import { getBrowserPage, resetEventData } from './utils.js';
import type { TestConfig } from './utils.js';

const testconfigs: Record<string, TestConfig> = {
    // p1 auto joins
    p1: { pageUrl: '/game/9999/leaderboard' },
    // start player 3 on the join page
    p3: { pageUrl: '/game/join', username: 'player_three', password: 'player_three' }
    // host: { pageUrl: '/host/9999', username: 'sample_admin', password: 'sample_admin' }
};

let p1: PlayerGamePage;
let p3: PlayerGamePage;
// let host: HostGamePage;

test.beforeEach(async ({ browser }) => {
    p1 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p1);
    p3 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p3);
    // host = new HostGamePage(await getBrowserPage(browser), testconfigs.host);
});

test.afterEach(async () => {
    await p1.logout();
    await p3.logout();
    // await host.logout();

    await resetEventData();
});

// TODO: actual locator (div w/ a classname?)
test.skip('player one leaderboard updates when another team joins', async () => {
    // expect player 1's team to be on the leaderboard, but not p3
    await expect(p1.page.locator('something')).toHaveText('p1 team name');
    await expect(p1.page.locator('something')).not.toHaveText('p3 team name');
    // p3 navigates to /game/9999
    p3.page.goto('/game/9999');
    // player 1 should now see player 3's team
    await expect(p1.page.locator('something')).toHaveText('p3 team name');
    // player 3 should see both teams
    await expect(p3.page.locator('something')).toHaveText('p1 team name');
    await expect(p3.page.locator('something')).toHaveText('p3 team name');
});

// TODO: test actual leaderboard updates (pts values) from the host, maybe tiebreakers here too
