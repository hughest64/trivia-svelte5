import { expect, test } from '@playwright/test';
import {
    PlayerGamePage
    // HostGamePage
} from './gamePages.js';
import { loginToGame, getBrowserPage, resetEventData, asyncTimeout } from './utils.js';
import type { TestConfig } from './utils.js';

const testconfigs: Record<string, TestConfig> = {
    // p1 auto joins
    p1: { pageUrl: '/game/9999', joincode: '9999' },
    // start player 3 on the join page
    p3: { pageUrl: '/game/join', joincode: '9999', username: 'player_three', password: 'player_three' }
    // host: { pageUrl: '/host/9999', username: 'sample_admin', password: 'sample_admin' }
};

let p1: PlayerGamePage;
let p3: PlayerGamePage;
// let host: HostGamePage;

test.beforeEach(async ({ browser }) => {
    // log p1 into the game directly
    p1 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p1);
    loginToGame(p1.page, testconfigs.p1);
    // log p3 in, but don't join the game just yet
    p3 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p3);
    p3.login();
    // host = new HostGamePage(await getBrowserPage(browser), testconfigs.host);
});

test.afterEach(async () => {
    await p1.logout();
    await p3.logout();
    // await host.logout();

    await resetEventData();
});

// TODO: actual locator (div w/ a classname?)
test('player one leaderboard updates when another team joins', async () => {
    // expect player 1's team to be on the leaderboard, but not p3
    await asyncTimeout();
    await expect(p1.page).toHaveURL('/game/9999');
    await p1.page.goto('/game/9999/leaderboard');
    await expect(p1.page).toHaveURL('/game/9999/leaderboard');
    await expect(p1.page.locator('h3.team-name', { hasText: /hello world/i })).toBeVisible();
    await expect(p1.page.locator('h3.team-name', { hasText: /for all the marbles/i })).not.toBeVisible();

    // TODO: this is proabably worthy of it's own helper function
    // p3 joins the game
    p3.page.goto('/game/join');
    await p3.page.locator('input[name="joincode"]').fill('9999' as string);
    await p3.page.locator('button[type="submit"]').click();
    p3.page.goto('/game/9999/leaderboard');
    await expect(p3.page).toHaveURL('/game/9999/leaderboard');

    // player 1 should now see player 3's team
    await expect(p1.page.locator('h3.team-name', { hasText: /for all the marbles/i })).toBeVisible();
    // player 3 should see both teams
    await expect(p3.page.locator('h3.team-name', { hasText: /hello world/i })).toBeVisible();
    await expect(p3.page.locator('h3.team-name', { hasText: /for all the marbles/i })).toBeVisible();
});

test('round headers on the leaderboard navigate back to the game', async () => {
    await asyncTimeout();
    await expect(p1.page).toHaveURL('/game/9999');
    await p1.page.goto('/game/9999/leaderboard');
    await expect(p1.page).toHaveURL('/game/9999/leaderboard');

    // click on round 5
    const rd5 = p1.page.locator('.round-selector').locator('button', { hasText: '5' });
    await rd5.click();
    // expect to be back on the game and round 5 is active
    await expect(p1.page).toHaveURL('/game/9999');
    await expect(rd5).toHaveClass('active');
});

// TODO: test actual leaderboard updates (pts values) from the host, maybe tiebreakers here too
