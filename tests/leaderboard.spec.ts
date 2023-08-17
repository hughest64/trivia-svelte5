import { test, expect } from './authConfigs.js';
import { createApiContext, checkLbEntry } from './utils.js';
import type { APIRequestContext } from '@playwright/test';

const joincode = '9900';
const eventUrl = `/game/${joincode}`;
const hostUrl = `/host/${joincode}`;
const leaderboardUrl = `${eventUrl}/leaderboard`;

let apicontext: APIRequestContext;

const game_data = {
    game_id: 15,
    joincode
};

test.beforeAll(async () => {
    apicontext = await createApiContext();
});

test.beforeEach(async ({ host }) => {
    // set up the event
    const response = await apicontext.post('ops/run-game/', {
        headers: await host.getAuthHeader(),
        data: { game_data: JSON.stringify(game_data) }
    });
    expect(response.status()).toBe(200);
});

test.afterEach(async ({ host }) => {
    // reset the team name for name change test
    const response = await apicontext.post('ops/reset-teamname/', {
        headers: await host.getAuthHeader(),
        data: {
            current_names: ['goodbye world'],
            new_names: ['hello world']
        }
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
    await expect(p1.page.locator('h3.team-name-display', { hasText: /hello world/i })).toBeVisible();
    await expect(p1.page.locator('h3.team-name-display', { hasText: /for all the marbles/i })).not.toBeVisible();

    // p3 joins the game
    await p3.joinGame(joincode);
    await p3.page.goto(leaderboardUrl);

    // player 1 should now see player 3's team
    await expect(p1.page.locator('h3.team-name-display', { hasText: /for all the marbles/i })).toBeVisible();

    // player 3 should see both teams
    await expect(p3.page.locator('h3.team-name-display', { hasText: /hello world/i })).toBeVisible();
    await expect(p3.page.locator('h3.team-name-display', { hasText: /for all the marbles/i })).toBeVisible();
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

test('points adjustment', async ({ p1, host }) => {
    await p1.joinGame(joincode);
    // lock round 1
    const r = await apicontext.post(`/ops/rlock/${joincode}/`, {
        headers: await host.getAuthHeader(),
        data: JSON.stringify({ round_number: 1, locked: true, type: 'round_lock' })
    });
    expect(r.status()).toBe(200);

    await p1.page.goto(leaderboardUrl);
    const playerlb = p1.page.locator('ul#player-leaderboard-view').locator('li.leaderboard-entry-container');
    const entry = playerlb.nth(0);
    // should have 0 pts initially
    await checkLbEntry(entry, { name: /hello world/i, rank: '-', points: '0' });

    await host.page.goto(`${hostUrl}/leaderboard`);
    const hostLbEntry = host.page.locator('button.team-name-btn', {
        has: host.page.locator('h3', { hasText: /hello world/i })
    });
    await expect(hostLbEntry).toBeVisible();
    await hostLbEntry.click();

    const teamNameBtn = host.page.locator('button.edit-teamname');
    await expect(teamNameBtn).toBeVisible();
    await teamNameBtn.click();

    // go up .5
    const plusBtn = host.page.locator('button#plus-btn');
    await expect(plusBtn).toBeVisible();
    plusBtn.click();

    // expect total to be + .5
    const ptTotal = host.page.locator('h3.points-display').first();
    await expect(ptTotal).toHaveText(/\.5/);

    // find reason
    await host.page.locator('select[name="adjustment_reason"]').selectOption('2');
    // set reason
    // do an api call to check for the reason
    const response = await apicontext.post('ops/validate/', {
        headers: await host.getAuthHeader(),
        data: {
            type: 'validate_pts_adj_reason',
            joincode,
            team_name: 'hello world',
            reason_id: 2
        }
    });
    expect(response.status()).toBe(200);

    // reveal answers, update public lb
    const revealBtn = host.page.locator('button#reveal-button');
    await expect(revealBtn).toBeVisible();
    await revealBtn.click();

    const syncBtn = host.page.locator('button#sync-button');
    await expect(syncBtn).toBeVisible();
    await syncBtn.click();

    // p1 should see the new pt total
    const updatedPlayerlb = p1.page.locator('ul#player-leaderboard-view').locator('li.leaderboard-entry-container');
    const updatedentry = updatedPlayerlb.nth(0);
    await checkLbEntry(updatedentry, { name: /hello world/i, rank: '1', points: /\.5/ });
});

test('a team can change their name', async ({ p1, host }) => {
    await p1.joinGame(joincode);
    await p1.page.goto(leaderboardUrl);
    await expect(p1.page).toHaveURL(leaderboardUrl);

    await host.page.goto(`${hostUrl}/leaderboard`);

    // find the hello world entry and click to expand it
    const lbEntry = p1.page.locator('button.team-name-btn', {
        has: p1.page.locator('h3', { hasText: /hello world/i })
    });
    await expect(lbEntry).toBeVisible();
    await lbEntry.click();

    // click the pencil icon
    const teamNameBtn = p1.page.locator('button.edit-teamname');
    await expect(teamNameBtn).toBeVisible();
    await teamNameBtn.click();

    const teamNameInput = p1.page.locator('input[name="team_name"]');
    await expect(teamNameInput).toBeVisible();
    await teamNameInput.fill('goodbye world');
    const submitBtn = p1.page.locator('button.edit-teamname');
    await expect(submitBtn).toBeVisible();
    await submitBtn.click();

    // expect host to see the change
    const hostLbEntry = host.page.locator('button.team-name-btn', {
        has: host.page.locator('h3', { hasText: /goodbye world/i })
    });
    await expect(hostLbEntry).toBeVisible();
});
/**
 * TODO:
 * factor in megaround scores at the end of the game
 *
 * test unlocking a round and allowing a player to update a response
 * - should re-autograde properly (but I was getting a 400 from the api)
 * - make sure respones for a round are unlocking when the round is unlocked
 */
