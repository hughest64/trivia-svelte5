import { test, expect } from '@playwright/test';
import { createApiContext } from './utils.js';
import { getUserPage, userAuthConfigs } from './authConfigs.js';
import type { APIRequestContext } from '@playwright/test';
import type { PlayerGamePage, HostGamePage } from './gamePages.js';

const joincode = '9907';
const hostUrl = `/host/${joincode}`;

const { playerOne, playerThree } = userAuthConfigs;

let apicontext: APIRequestContext;
let p1: PlayerGamePage;
let host: HostGamePage;

const game_data = {
    joincode,
    reset_event: true,
    teams: 2,
    rounds_to_play: 1,
    team_configs: {
        '1': {
            name: playerOne.teamName,
            players: [playerOne.username],
            questions: {
                '1.1': { answer: 'football', points: 0 },
                '1.2': { answer: 'candy corn', points: 0 }
            }
        },
        '2': {
            name: playerThree.teamName,
            players: [playerThree.username],
            questions: {
                '1.1': { answer: 'football', points: 0 },
                '1.2': { answer: 'cinnamon rolls', points: 1 }
            }
        }
    },
    host_config: { lock_rounds: true }
};

test.beforeAll(async ({ browser }) => {
    apicontext = await createApiContext();
    p1 = (await getUserPage(browser, 'playerOne')) as PlayerGamePage;
    host = (await getUserPage(browser, 'host')) as HostGamePage;
});

test.afterAll(async () => {
    await p1.page.context().close();
    await host.page.context().close();
    await apicontext.dispose();
});

test.beforeEach(async () => {
    await apicontext.post('/ops/run-game/', {
        headers: await host.getAuthHeader(),
        data: { game_data: JSON.stringify(game_data) }
    });
});

test('scoring updates properly update the leaderboards', async () => {
    await host.page.goto(hostUrl);

    // click "score this round"
    const scoreBtn = host.page.locator('a', { hasText: 'Score This Round' });
    // should exist w/ that text
    await expect(scoreBtn).toBeVisible();
    await scoreBtn.click();
    await expect(host.page).toHaveURL(`${hostUrl}/score`);

    const nextBtn = host.page.locator('button', { hasText: 'Next' }).first();
    await expect(nextBtn).toBeVisible();

    const ptsList = host.page.locator('ul#response-groups').locator('li.scoring-response');
    await expect(ptsList).toHaveCount(1);

    const funnyBtn = host.page.locator('button.funny-button');
    const ptsBtn = host.page.locator('button.score-icon');

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

    await host.page.goto(`${hostUrl}/leaderboard`);

    // host lb should update automatically
    const hostlb = host.page.locator('ul#host-leaderboard-view').locator('li.leaderboard-entry-container');
    await expect(hostlb).toHaveCount(2);
    const hostEntry1 = hostlb.nth(0);
    await expect(hostEntry1.locator('h3.team-name')).toHaveText(/for all the marbles/i);
    await expect(hostEntry1.locator('h3.rank')).toHaveText('1');
    await expect(hostEntry1.locator('h3.points')).toHaveText('2');
    const hostEntry2 = hostlb.nth(1);
    await expect(hostEntry2.locator('h3.team-name')).toHaveText(/hello world/i);
    await expect(hostEntry2.locator('h3.rank')).toHaveText('2');
    await expect(hostEntry2.locator('h3.points')).toHaveText('1');
});

// TODO: this should really be in leaderboard.spec
test('host reveal questions to players', async () => {
    // p1 should not see answer summary
    await p1.page.goto(`/game/${joincode}`);
    const answerSummary = p1.page.locator('div.answer-summary');
    await expect(answerSummary).not.toBeVisible();

    // reveal the answers to the player
    await host.page.goto(`${hostUrl}/leaderboard`);
    const revealBtn = host.page.locator('button#reveal-button');
    await expect(revealBtn).toBeVisible();
    await revealBtn.click();

    const answer = answerSummary.locator('p', { hasText: /correct answer/i });
    const points = answerSummary.locator('p', { hasText: /you received/i });
    const funny = answerSummary.locator('p', { hasText: /funny answer/i });

    // validate the answer summary
    await expect(answerSummary).toBeVisible();
    await expect(answer).toBeVisible();
    await expect(points).toHaveText(/0 pt/);
    await expect(funny).not.toBeVisible();
});

// TODO: add test for the stats bar (once it's finalized)
