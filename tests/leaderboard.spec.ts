import { test, expect } from './fixtures.js';
import { resetEventData } from './utils.js';

const joincode = '9900';
const eventUrl = `/game/${joincode}`;
const hostUrl = `/host/${joincode}`;
const leaderboardUrl = `${eventUrl}/leaderboard`;

test.beforeEach(async () => {
    await resetEventData({ joincodes: joincode });
});

// test.afterAll(async () => {
//     await resetEventData({ joincodes: joincode });
// });

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

    // TODO: test host leaderboard also updates when teams join
});

test('leaderboards update properly', async ({ p1Page, p3Page, hostPage }) => {
    // host reveals r1q1
    await hostPage.page.goto(hostUrl);
    await hostPage.revealQuestion('1.1');

    // p1 & p3 each answer the same question (1 correct 1 incorrect)
    await p1Page.joinGame(joincode);
    await p3Page.joinGame(joincode);

    await p1Page.setResponse('baseball', { submit: true });
    await p3Page.setResponse('basketball', { submit: true });

    // host locks the round and goes to leaderboard
    await hostPage.lockIconLabel('1').click();
    const scoreBtn = hostPage.page.locator('a', { hasText: 'Score This Round' });
    await expect(scoreBtn).toBeVisible();
    await hostPage.page.goto(`${hostUrl}/score`);
    // expect host lb to have p1 w/ rank 1, 1pt & p3 w/ rank '-', 0 pts

    // host goes back to quiz and clicks "score this round"
    await hostPage.page.goto(hostUrl);
    await scoreBtn.click();
});
// change p3 score to 1/2
// expect rank 2, 1/2 pts
// change p2 score to 1
// expect both to have rank 1, 1 pt
// should we test ordering?
// host click public leaderboard
// expect no ranks or pts
// expect sync btn to be visible
// host click sync btn
// expect btn to disappear
// expect both to teams to have rank 1, pts 1
// expect players to see the same on the lb page

test('round headers on the leaderboard navigate back to the game', async ({ p1Page }) => {
    // await p1Page.joinGame(joincode);/
    await p1Page.page.goto(leaderboardUrl);
    await expect(p1Page.page).toHaveURL(leaderboardUrl);
    // click on round 5
    const rd1 = p1Page.page.locator('.round-selector').locator('button', { hasText: '1' });
    await rd1.click();
    // expect to be back on the game and round 5 is active
    await expect(p1Page.page).toHaveURL(eventUrl);
    await expect(rd1).toHaveClass(/active/);
    // TODO: expect player to see there answer/pts awarded on the quiz pg for the question
});

// TODO:
// test unlocking a round and allowing a player to update a response
// - should re-autograde properly (but I was getting a 400 from the api)
// - make sure respones for a round are unlocking when the round is unlocked
// test clicking score this round goes to scoring and shows grouped resps
