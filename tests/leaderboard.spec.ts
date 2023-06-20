import { test, expect } from './authConfigs.js';
import { createApiContext, checkLbEntry } from './utils.js';
import type { APIRequestContext } from '@playwright/test';

// TODO: factor in megaround scores at the end of the game

const joincode = '9900';
const eventUrl = `/game/${joincode}`;
const hostUrl = `/host/${joincode}`;
const leaderboardUrl = `${eventUrl}/leaderboard`;

let apicontext: APIRequestContext;

const game_data = {
    game_id: 15,
    joincode
};

test.beforeAll(async ({ host }) => {
    apicontext = await createApiContext();
    // set up the event
    const response = await apicontext.post('ops/run-game/', {
        headers: await host.getAuthHeader(),
        data: { game_data: JSON.stringify(game_data) }
    });
    expect(response.status()).toBe(200);
});

test.afterAll(async () => {
    apicontext.dispose();
});

test('player one leaderboard updates when another team joins', async ({ p1, p3 }) => {
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

test('host leaderboard updates on round lock, public updates on btn click', async ({ p1, p3, host }) => {
    // p1 & p3 each answer the same question (1 correct 1 incorrect)
    await p1.joinGame(joincode);
    await p3.joinGame(joincode);

    // incorrect answer
    await p1.setResponse('football', { submit: true });
    // correct answer
    await p3.setResponse('basketball', { submit: true });

    // lock the round
    const r = await apicontext.post(`/ops/rlock/${joincode}/`, {
        headers: await host.getAuthHeader(),
        data: JSON.stringify({ round_number: 1, locked: true, type: 'round_lock' })
    });
    expect(r.status()).toBe(200);

    await p1.page.goto(`${eventUrl}/leaderboard`);

    // host reveal answers to players (required before snycing leaderboards)
    await host.page.goto(`${hostUrl}/leaderboard`);
    const revealBtn = host.page.locator('button#reveal-button');
    await expect(revealBtn).toBeVisible();
    await revealBtn.click();

    // expect host lb to have p1 w/ rank 1, 1pt & p3 w/ rank '-', 0 pts
    const hostlb = host.page.locator('ul#host-leaderboard-view').locator('li.leaderboard-entry-container');
    await expect(hostlb).toHaveCount(2);
    // 1st place
    const hostEntry1 = hostlb.nth(0);
    await checkLbEntry(hostEntry1, { name: /for all the marbles/i, rank: '1', points: '1' });
    // not ranked
    const hostEntry2 = hostlb.nth(1);
    await checkLbEntry(hostEntry2, { name: /hello world/i, rank: '-', points: '0' });

    // public leaderboard has not been updated
    await host.page.locator('button#public-view').click();
    const publiclb = host.page.locator('ul#public-leaderboard-view').locator('li.leaderboard-entry-container');
    await expect(publiclb).toHaveCount(2);
    // not ranked
    const pubEntry2 = publiclb.nth(0);
    await checkLbEntry(pubEntry2, { name: /hello world/i, rank: '-', points: '0' });
    // not ranked
    const pubEntry1 = publiclb.nth(1);
    await checkLbEntry(pubEntry1, { name: /for all the marbles/i, rank: '-', points: '0' });

    // sync the leaderboards
    await host.page.locator('button#host-view').click();
    const syncBtn = host.page.locator('button#sync-button');
    await expect(syncBtn).toBeVisible();
    await syncBtn.click();

    await host.page.locator('button#public-view').click();
    await expect(host.page.locator('button#sync-button')).not.toBeVisible();

    const updatedPubliclb = host.page.locator('ul#public-leaderboard-view').locator('li.leaderboard-entry-container');
    // 1st place
    const updatedPubEntry1 = updatedPubliclb.nth(0);
    await checkLbEntry(updatedPubEntry1, { name: /for all the marbles/i, rank: '1', points: '1' });
    // not ranked
    const updatedPubEntry2 = updatedPubliclb.nth(1);
    await checkLbEntry(updatedPubEntry2, { name: /hello world/i, rank: '-', points: '0' });

    const playerlb = p1.page.locator('ul#player-leaderboard-view').locator('li.leaderboard-entry-container');
    await expect(playerlb).toHaveCount(2);
    // 1st place
    const p1entry1 = playerlb.nth(0);
    await checkLbEntry(p1entry1, { name: /for all the marbles/i, rank: '1', points: '1' });
    // not ranked
    const p1entry2 = playerlb.nth(1);
    await checkLbEntry(p1entry2, { name: /hello world/i, rank: '-', points: '0' });
});

// TODO: with the new implementation, this has trouble with auth but not all the time, why?
test('round headers on the leaderboard navigate back to the game', async ({ p1 }) => {
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