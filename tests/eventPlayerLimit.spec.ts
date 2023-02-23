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
    // start player 2 on the join page
    p2: { pageUrl: '/game/join', username: 'player_two', password: 'player_two' }
};

let p1: PlayerGamePage;
let p2: PlayerGamePage;
// let host: HostGamePage;

test.beforeEach(async ({ browser }) => {
    p1 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p1);
    p2 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p3);
});

test.afterEach(async () => {
    await p1.logout();
    await p2.logout();
    await resetEventData();
});

test.skip('player two cannot join the event due to a player limit', async () => {
    expect(true);
    // test via join expect error message on join page
    // p2 enter joincode 9999
    // expect error page
    // p2 direct navigate to /game/9999
    // expect error
    // click a button
    // expect correct page
    // click back
    // click other button
    // expect correct page
});
