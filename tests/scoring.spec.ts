import { test, expect } from './fixtures.js';
import { asyncTimeout, resetEventData } from './utils.js';

const joincode = '9907';
// const eventUrl = `/game/${joincode}`;
const hostUrl = `/host/${joincode}`;
// const leaderboardUrl = `${eventUrl}/leaderboard`;

test.beforeEach(async () => {
    await resetEventData({ joincodes: joincode });
});

// TODO:
// - answer two questions (different answers on q2)
// - mark q2 for p1 as funny (but not p3)
// - make sure to cycle through from 0 -> .5 -> 1 for pts
// - p1 should check q1 and q2 for both pts and funny
test('scoring updates properly update the leaderboards', async ({ p1Page, p3Page, hostPage }) => {
    /// p1 & p3 each answer the same question (1 correct 1 incorrect)
    await p1Page.joinGame(joincode);
    await p3Page.joinGame(joincode);

    // TODO: answer multiple questions?
    // incorrect answer
    await p1Page.setResponse('football', { submit: true });
    await p3Page.setResponse('football', { submit: true });

    // lock the round
    await hostPage.page.goto(hostUrl);
    await hostPage.lockIconLabel('1').click();
    await asyncTimeout(500);

    // p1 should not see answer summary
    const answerSummary = p1Page.page.locator('div.answer-summary');
    await expect(answerSummary).not.toBeVisible();

    // click "score this round"
    const scoreBtn = hostPage.page.locator('a', { hasText: 'Score This Round' });
    // should exist w/ that text
    await expect(scoreBtn).toBeVisible();
    await scoreBtn.click();
    await expect(hostPage.page).toHaveURL(`${hostUrl}/score`);
    // should be one group not correct, not funny
    // mark to give 1/2 credit
    // mark to make funny
    await hostPage.page.goto(`${hostUrl}/leaderboard`);
    // host lb should reflect the 1/2 pt for both teams
    const syncBtn = hostPage.page.locator('button#sync-button');
    await expect(syncBtn).toBeVisible();
    await syncBtn.click();

    // expect to see pts summary (.pts, marked as funny)
    await expect(answerSummary).toBeVisible();
});
