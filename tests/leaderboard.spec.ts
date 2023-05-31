import { test, /* request, */ expect } from '@playwright/test';
import { asyncTimeout, resetEventData } from './utils.js';
// import type { APIRequestContext } from '@playwright/test';
import type { PlayerGamePage, HostGamePage } from './gamePages.js';
import { getUserPage } from './authConfigs.js';

// TODO: refactor to use the new api game_runner, also factor in megaround scores at the end of the game

const joincode = '9900';
const eventUrl = `/game/${joincode}`;
const hostUrl = `/host/${joincode}`;
const leaderboardUrl = `${eventUrl}/leaderboard`;

let p1: PlayerGamePage;
let p3: PlayerGamePage;
let host: HostGamePage;

test.beforeAll(async ({ browser }) => {
    p1 = (await getUserPage(browser, 'playerOne')) as PlayerGamePage;
    p3 = (await getUserPage(browser, 'playerThree')) as PlayerGamePage;
    host = (await getUserPage(browser, 'host')) as HostGamePage;
});

test.afterAll(async () => {
    // apicontext.dispose();
    await p1.page.context().close();
    await p3.page.context().close();
    await host.page.context().close();
});

test.beforeEach(async () => {
    await resetEventData({ joincodes: joincode });
});

// test.afterEach(async () => {
//     await resetEventData({ joincodes: joincode });
// });

test('player one leaderboard updates when another team joins', async () => {
    await p1.joinGame(joincode);
    await p1.page.goto(leaderboardUrl);
    await expect(p1.page).toHaveURL(leaderboardUrl);

    // expect player 1's team to be on the leaderboard, but not p3
    await expect(p1.page.locator('h3.team-name', { hasText: /hello world/i })).toBeVisible();
    await expect(p1.page.locator('h3.team-name', { hasText: /for all the marbles/i })).not.toBeVisible();

    // p3 joins the game
    await p3.joinGame(joincode);
    await p3.page.goto(leaderboardUrl);

    // player 1 should now see player 3's team
    await expect(p1.page.locator('h3.team-name', { hasText: /for all the marbles/i })).toBeVisible();

    // player 3 should see both teams
    await expect(p3.page.locator('h3.team-name', { hasText: /hello world/i })).toBeVisible();
    await expect(p3.page.locator('h3.team-name', { hasText: /for all the marbles/i })).toBeVisible();
});

// TODO: a helper for checking each entry would be great!
test('host leaderboard updates on round lock, public updates on btn click', async () => {
    // host reveals r1q1
    await host.page.goto(hostUrl);

    // p1 & p3 each answer the same question (1 correct 1 incorrect)
    await p1.joinGame(joincode);
    await p3.joinGame(joincode);

    // incorrect answer
    await p1.setResponse('football', { submit: true });
    // correct answer
    await p3.setResponse('basketball', { submit: true });

    await p1.page.goto(`${eventUrl}/leaderboard`); // TODO: we should probably click the link in the footer

    // host locks the round and goes to leaderboard
    await host.lockIconLabel('1').click();
    await asyncTimeout(500);
    await host.page.goto(`${hostUrl}/leaderboard`);

    const revealBtn = host.page.locator('button#reveal-button');
    await expect(revealBtn).toBeVisible();
    await revealBtn.click();
    // TODO: should we check for answer reveal player side here?

    // expect host lb to have p1 w/ rank 1, 1pt & p3 w/ rank '-', 0 pts
    const hostlb = host.page.locator('ul#host-leaderboard-view').locator('li.leaderboard-entry-container');
    await expect(hostlb).toHaveCount(2);
    // 1st place
    const hostEntry1 = hostlb.nth(0);
    await expect(hostEntry1.locator('h3.team-name')).toHaveText(/for all the marbles/i);
    await expect(hostEntry1.locator('h3.rank')).toHaveText('1');
    await expect(hostEntry1.locator('h3.points')).toHaveText('1');
    // not ranked
    const hostEntry2 = hostlb.nth(1);
    await expect(hostEntry2.locator('h3.team-name')).toHaveText(/hello world/i);
    await expect(hostEntry2.locator('h3.rank')).toHaveText('-');
    await expect(hostEntry2.locator('h3.points')).toHaveText('0');

    // public leaderboard has not been updated
    await host.page.locator('button#public-view').click();
    const publiclb = host.page.locator('ul#public-leaderboard-view').locator('li.leaderboard-entry-container');
    await expect(publiclb).toHaveCount(2);
    // not ranked
    const pubEntry2 = publiclb.nth(0);
    await expect(pubEntry2.locator('h3.team-name')).toHaveText(/hello world/i);
    await expect(pubEntry2.locator('h3.rank')).toHaveText('-');
    await expect(pubEntry2.locator('h3.points')).toHaveText('0');
    // not ranked
    const pubEntry1 = publiclb.nth(1);
    await expect(pubEntry1.locator('h3.team-name')).toHaveText(/for all the marbles/i);
    await expect(pubEntry1.locator('h3.rank')).toHaveText('-');
    await expect(pubEntry1.locator('h3.points')).toHaveText('0');

    // sync the leaderboards
    await host.page.locator('button#host-view').click();

    const syncBtn = host.page.locator('button#sync-button');
    await expect(syncBtn).toBeVisible();
    await syncBtn.click();

    await host.page.locator('button#public-view').click();
    await expect(host.page.locator('button#sync-button')).not.toBeVisible();

    const updatedPubliclb = host.page.locator('ul#public-leaderboard-view').locator('li.leaderboard-entry-container');
    const updatedPubEntry1 = updatedPubliclb.nth(0);
    await expect(updatedPubEntry1.locator('h3.team-name')).toHaveText(/for all the marbles/i);
    await expect(updatedPubEntry1.locator('h3.rank')).toHaveText('1');
    await expect(updatedPubEntry1.locator('h3.points')).toHaveText('1');
    // not ranked
    const updatedPubEntry2 = updatedPubliclb.nth(1);
    await expect(updatedPubEntry2.locator('h3.team-name')).toHaveText(/hello world/i);
    await expect(updatedPubEntry2.locator('h3.rank')).toHaveText('-');
    await expect(updatedPubEntry2.locator('h3.points')).toHaveText('0');

    const playerlb = p1.page.locator('ul#player-leaderboard-view').locator('li.leaderboard-entry-container');
    await expect(playerlb).toHaveCount(2);
    const p1entry1 = playerlb.nth(0);
    await expect(p1entry1.locator('h3.team-name')).toHaveText(/for all the marbles/i);
    await expect(p1entry1.locator('h3.rank')).toHaveText('1');
    await expect(p1entry1.locator('h3.points')).toHaveText('1');
    // not ranked
    const p1entry2 = playerlb.nth(1);
    await expect(p1entry2.locator('h3.team-name')).toHaveText(/hello world/i);
    await expect(p1entry2.locator('h3.rank')).toHaveText('-');
    await expect(p1entry2.locator('h3.points')).toHaveText('0');
});

test('round headers on the leaderboard navigate back to the game', async () => {
    // await p1.joinGame(joincode);/
    await p1.page.goto(leaderboardUrl);
    await expect(p1.page).toHaveURL(leaderboardUrl);
    // click on round 5
    const rd1 = p1.page.locator('.round-selector').locator('button', { hasText: '1' });
    await rd1.click();
    // expect to be back on the game and round 5 is active
    await expect(p1.page).toHaveURL(eventUrl);
    await expect(rd1).toHaveClass(/active/);
});

// TODO:
// test unlocking a round and allowing a player to update a response
// - should re-autograde properly (but I was getting a 400 from the api)
// - make sure respones for a round are unlocking when the round is unlocked
