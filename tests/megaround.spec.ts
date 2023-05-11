import { test, request, expect } from '@playwright/test';
import type { APIRequestContext } from '@playwright/test';
import { PlayerGamePage, getPageFromContext } from './gamePages.js';

const api_port = process.env.API_PORT || '7000';

let apicontext: APIRequestContext;
let player: PlayerGamePage;

const game_data = {
    game_id: null,
    joincode: 7812,
    teams: 1,
    use_score_percentage: true,
    rounds_to_play: 8,
    reuse: true,
    team_configs: {
        '1': {
            score_percentage: 80,
            megaround: { round: 6, values: { '1': 1, '2': 2, '3': 3, '4': 4, '5': 5 } }
        }
    }
};

test.beforeAll(async ({ browser }) => {
    // set up our user and authenticate if necessary
    const storagePath = 'playwright/.auth/some_user.json';
    const { page, userCookies } = await getPageFromContext(browser, storagePath);

    player = new PlayerGamePage(page, {
        username: 'run_game_user_1',
        password: '12345',
        authStoragePath: storagePath,
        cookies: userCookies
    });
    await player.useAuthConfig();

    // set up the evnet data
    apicontext = await request.newContext({ baseURL: `http://localhost:${api_port}` });

    const response = await apicontext.post('/run-game', {
        headers: { 'content-type': 'application/json', accept: 'application/json' },
        data: { secret: 'todd is great', game_data: JSON.stringify(game_data) }
    });

    expect(response.status()).toBe(200);
});

test.afterAll(async () => {
    apicontext.dispose();
    await player.page.context().close();
});

test('the megaround updates properly', async () => {
    await player.page.goto('/game/7812/megaround');
    await expect(player.page).toHaveURL('/game/7812/megaround');

    const rdSelector = player.page.locator('div.round-selector');
    // only 2nd half rounds are available
    await expect(rdSelector.locator('button')).toHaveCount(4);
    await expect(rdSelector.locator('button').first()).toHaveText(/5/);
    await expect(rdSelector.locator('button').last()).toHaveText(/8/);

    const mrInputs = player.page.locator('div.input-container');
    await expect(mrInputs.locator('#megaround-weight-1')).toHaveValue('1');
    await rdSelector.locator('button', { hasText: /8/ }).click();
    await expect(mrInputs.locator('#megaround-weight-1')).toBeEmpty();
    const submitBtn = player.page.locator('button', { hasText: /submit/i });
    await expect(submitBtn).toBeDisabled();

    const mrWeightOpts = player.page.locator('div.megaround-weight-selector');

    for (let i = 1; i <= 5; i++) {
        const btnLoc = mrWeightOpts.locator('button', { hasText: new RegExp(String(i)) });
        await expect(btnLoc).toBeVisible();
        await btnLoc.click();
        await expect(mrInputs.locator(`#megaround-weight-${i}`)).toHaveValue(String(i));
    }

    await expect(submitBtn).toBeEnabled();
    await submitBtn.click();

    // validate the we've update the selected megaround in the database
    const response = await apicontext.post('/validate', {
        headers: { 'content-type': 'application/json', accept: 'application/json' },
        // rd 8 should be the megaround for team 1
        data: { secret: 'todd is great', type: 'megaround', round: 8, team: 1, joincode: 7812 }
    });
    // for simplicity the api should return a 400 if something doesn't line up, 200 otherwise
    expect(response.status()).toBe(200);
});

test('a player cannot see locked megarounds', async () => {
    const response = await apicontext.post('/validate', {
        headers: { 'content-type': 'application/json', accept: 'application/json' },
        // rd 8 should be the megaround for team 1
        data: { secret: 'todd is great', type: 'megaround_lock', joincode: 7812 }
    });
    expect(response.status()).toBe(200);

    await player.page.goto('/game/7812/megaround');
    await expect(player.page).toHaveURL('/game/7812/megaround');

    await expect(player.page.locator('div.round-selector')).not.toBeVisible();
});
