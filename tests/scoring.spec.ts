import { test, expect } from './fixtures.js';
import { asyncTimeout, resetEventData } from './utils.js';

const joincode = '9907';
const hostUrl = `/host/${joincode}`;

test.beforeEach(async () => {
    await resetEventData({ joincodes: joincode });
});

test('scoring updates properly update the leaderboards', async ({ p1Page, p3Page, hostPage }) => {
    await p1Page.joinGame(joincode);
    await p3Page.joinGame(joincode);
    // incorrect answer
    await p1Page.setResponse('football', { submit: true });
    await p3Page.setResponse('football', { submit: true });
    await p1Page.goToQuestion('1.2');
    await p3Page.goToQuestion('1.2');
    await asyncTimeout(500);
    // incorrect
    await p1Page.setResponse('candy corn', { submit: true });
    // correct
    await p3Page.setResponse('cinammon rolls', { submit: true });

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

    const nextBtn = hostPage.page.locator('button', { hasText: 'Next' }).first();
    await expect(nextBtn).toBeVisible();
    // const prevBtn = hostPage.page.locator('button', { hasText: 'Previous' }).first();
    const ptsList = hostPage.page.locator('ul#response-groups').locator('li.scoring-response');
    const funnyBtn = hostPage.page.locator('button.funny-button');
    const ptsBtn = hostPage.page.locator('button.score-icon');

    await expect(ptsList).toHaveCount(1);
    await expect(ptsBtn.nth(0)).toHaveText('0 pts');
    await expect(funnyBtn.nth(0)).toHaveText(/not/i);

    // update the points
    await ptsBtn.nth(0).click();
    await expect(ptsBtn.nth(0)).toHaveText('0.5 pts');
    await ptsBtn.nth(0).click();
    await expect(ptsBtn.nth(0)).toHaveText('1 pts');

    // change questions, update funny
    await nextBtn.click();
    await expect(ptsList).toHaveCount(2);
    await funnyBtn.nth(1).click();
    await expect(funnyBtn.nth(1)).not.toHaveText(/not/i);

    await hostPage.page.goto(`${hostUrl}/leaderboard`);
    // host lb should reflect the 1/2 pt for both teams
    const syncBtn = hostPage.page.locator('button#sync-button');
    await expect(syncBtn).toBeVisible();

    // host lb should update automatically
    const hostlb = hostPage.page.locator('ul#host-leaderboard-view').locator('li.leaderboard-entry-container');
    await expect(hostlb).toHaveCount(2);
    const hostEntry1 = hostlb.nth(0);
    await expect(hostEntry1.locator('h3.team-name')).toHaveText(/for all the marbles/i);
    await expect(hostEntry1.locator('h3.rank')).toHaveText('1');
    await expect(hostEntry1.locator('h3.points')).toHaveText('2');
    const hostEntry2 = hostlb.nth(1);
    await expect(hostEntry2.locator('h3.team-name')).toHaveText(/hello world/i);
    await expect(hostEntry2.locator('h3.rank')).toHaveText('2');
    await expect(hostEntry2.locator('h3.points')).toHaveText('1');

    await syncBtn.click();
    const answer = answerSummary.locator('p', { hasText: /correct answer/i });
    const points = answerSummary.locator('p', { hasText: /you received/i });
    const funny = answerSummary.locator('p', { hasText: /funny answer/i });

    // p1 is currently on question 2
    await expect(answer).toHaveText(/rolls/i);
    await expect(points).toHaveText(/0 pts/);
    await expect(funny).toBeVisible();

    // got to question 1
    await expect(answerSummary).toBeVisible();
    await p1Page.goToQuestion('1.1');
    await asyncTimeout(500);
    await expect(answer).toBeVisible();
    await expect(points).toHaveText(/1 pt/);
    await expect(funny).not.toBeVisible();
});
