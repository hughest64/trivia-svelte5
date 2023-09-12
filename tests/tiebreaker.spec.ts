import { test, expect } from './authConfigs.js';
import { createApiContext, checkLbEntry } from './utils.js';
import { userAuthConfigs } from './authConfigs.js';
import type { APIRequestContext } from '@playwright/test';

const joincode = '9908';
const hostUrl = `/host/${joincode}`;
const leaderboardUrl = `${hostUrl}/leaderboard`;

const { playerOne, playerThree } = userAuthConfigs;

let apicontext: APIRequestContext;

const game_data = {
    joincode,
    rounds_to_play: 4,
    teams: 3,
    team_configs: {
        '1': { score_percentage: 80, name: playerOne.teamName },
        '2': { score_percentage: 80, name: playerThree.teamName },
        '3': { score_percentage: 60, name: 'Tiebreaker Team 3' }
    },
    host_config: {
        lock_rounds: true
    }
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

test.afterAll(async () => {
    apicontext.dispose();
});

test('ties initially show the same rank', async ({ host }) => {
    await host.page.goto(leaderboardUrl);

    // check that the first two teams have a rank of 1 and pts 0f 20
    const hostlb = host.page.locator('ul#host-leaderboard-view').locator('li.leaderboard-entry-container');
    // tied for 1st place
    const hostEntry1 = hostlb.nth(0);
    await checkLbEntry(hostEntry1, { name: /hello world/i, rank: '1', points: '20' });

    const hostEntry2 = hostlb.nth(1);
    await checkLbEntry(hostEntry2, { name: /for all the marbles/i, rank: '1', points: '20' });

    // 3rd place
    const hostEntry3 = hostlb.nth(2);
    await checkLbEntry(hostEntry3, { name: /tiebreaker team 3/i, rank: '3', points: '15' });

    // check that there is only one tb button
    const resolveBtn = host.page.locator('a', { hasText: /resolve tie/i });
    await expect(resolveBtn).toHaveCount(1);
    await resolveBtn.click();
    // validate the url
    await expect(host.page).toHaveURL(/\/controlboard/);
    // answer questions and submit
    // api call to get the correct answer
    const response = await apicontext.post('ops/validate/', {
        headers: await host.getAuthHeader(),
        data: { type: 'get_tb_answer', joincode, index: 0 }
    });
    expect(response.status()).toBe(200);
    const responseData = await response.json();
    const answer = Number(responseData?.answer) || 0;
    const p1Answer = String(answer + 1);
    const p2Answer = String(answer + 2);
    // answer the questions
    const tbInputs = host.page.locator('input.tiebreaker-answer');
    await expect(tbInputs).toHaveCount(2);
    await tbInputs.nth(0).fill(p1Answer);
    await tbInputs.nth(1).fill(p2Answer);
    const submitBtn = host.page.locator('button', { hasText: /apply tiebreaker/i });
    await expect(submitBtn).toHaveCount(1);
    await submitBtn.click();

    // navigage back to leaderboard
    const lbLink = host.page.locator('a', { hasText: /leaderboard/i });
    await expect(lbLink).toBeVisible();
    await lbLink.click();
    await expect(host.page).toHaveURL(/leaderboard$/);
    // validate ranks update but points are the same
    const hostlbUpdate1 = host.page.locator('ul#host-leaderboard-view').locator('li.leaderboard-entry-container');
    // 1st place
    const hostEntry1Update1 = hostlbUpdate1.nth(0);
    await checkLbEntry(hostEntry1Update1, { name: /hello world/i, rank: '1', points: '20' });
    // 2nd place
    const hostEntry2Update1 = hostlbUpdate1.nth(1);
    await checkLbEntry(hostEntry2Update1, { name: /for all the marbles/i, rank: '2', points: '20' });
    // 3rd place
    const hostEntry3Update1 = hostlbUpdate1.nth(2);
    await checkLbEntry(hostEntry3Update1, { name: /tiebreaker team 3/i, rank: '3', points: '15' });

    // lock rd 5
    const quizLink = host.page.locator('a', { hasText: /quiz/i });
    await expect(quizLink).toBeVisible();
    await quizLink.click();
    await host.roundButton('5').click();
    await host.lockIconLabel('5').click();
    await lbLink.click();

    // ties are back since no other questions have been answered and a new round has been locked
    const hostlbUpdate2 = host.page.locator('ul#host-leaderboard-view').locator('li.leaderboard-entry-container');
    // 1st place
    const hostEntry1Update2 = hostlbUpdate2.nth(0);
    await checkLbEntry(hostEntry1Update2, { name: /hello world/i, rank: '1', points: '20' });
    // 2nd place
    const hostEntry2Update2 = hostlbUpdate2.nth(1);
    await checkLbEntry(hostEntry2Update2, { name: /for all the marbles/i, rank: '2', points: '20' });
    // 3rd place
    const hostEntry3Update2 = hostlbUpdate2.nth(2);
    await checkLbEntry(hostEntry3Update2, { name: /tiebreaker team 3/i, rank: '3', points: '15' });
});

// TODO: additional test(s) for:
// validate new rank info is displayed
// refresh the page
// validate that resps are populated
// change questions
// validate resps are not populated
