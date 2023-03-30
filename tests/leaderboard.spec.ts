import { test, expect } from './fixtures.js';
import { resetEventData } from './utils.js';

const joincode = '9900';
const eventUrl = `/game/${joincode}`;
const leaderboardUrl = `${eventUrl}/leaderboard`;

test.beforeEach(async () => {
    await resetEventData({ joincodes: joincode });
});

test('player one leaderboard updates when another team joins', async ({ p1Page, p3Page }) => {
    await p1Page.joinGame(joincode);
    await p1Page.page.goto(leaderboardUrl);
    await expect(p1Page.page).toHaveURL(leaderboardUrl);

    // expect player 1's team to be on the leaderboard, but not p3
    await expect(p1Page.page.locator('h3.team-name', { hasText: /hello world/i })).toBeVisible();
    await expect(p1Page.page.locator('h3.team-name', { hasText: /for all the marbles/i })).not.toBeVisible();

    // p3 joins the game
    await p3Page.joinGame(joincode);
    await p3Page.page.goto(leaderboardUrl);

    // player 1 should now see player 3's team
    await expect(p1Page.page.locator('h3.team-name', { hasText: /for all the marbles/i })).toBeVisible();

    // player 3 should see both teams
    await expect(p3Page.page.locator('h3.team-name', { hasText: /hello world/i })).toBeVisible();
    await expect(p3Page.page.locator('h3.team-name', { hasText: /for all the marbles/i })).toBeVisible();
});

test('round headers on the leaderboard navigate back to the game', async ({ p1Page }) => {
    await p1Page.joinGame(joincode);
    await p1Page.page.goto(leaderboardUrl);
    await expect(p1Page.page).toHaveURL(leaderboardUrl);
    // click on round 5
    const rd5 = p1Page.page.locator('.round-selector').locator('button', { hasText: '5' });
    await rd5.click();
    // expect to be back on the game and round 5 is active
    await expect(p1Page.page).toHaveURL(eventUrl);
    await expect(rd5).toHaveClass('active');
});

// TODO:
// test host leaderboard also updates when teams join
// test host leaderboard public vs. host views
// test host leaderboard when update btn should and should not appear
// test actual leaderboard updates (pts values) from the host, maybe tiebreakers here too
// test host leaderboard updates independently of the public leaderboard (scoring, tibebreakers, etc)
// test that the public leaderboard updates when the host clicks "update leaderboard"
// test pts/funny/answers visible after scoring a round but not before
// test unlocking a round and allowing a player to update a response
// - should re-autograde properly (but I was getting a 400 from the api)
// - make sure respones for a round are unlocking when the round is unlocked
// test clicking score this round goes to scoring and shows grouped resps
