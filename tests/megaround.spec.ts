import type { APIRequestContext } from '@playwright/test';
import { createApiContext } from './utils.js';
import { userAuthConfigs, test, expect } from './authConfigs.js';

let apicontext: APIRequestContext;

const { playerOne } = userAuthConfigs;

const game_data = {
    game_id: null,
    joincode: 7812,
    teams: 1,
    rounds_to_play: 8,
    team_configs: {
        '1': {
            name: playerOne.teamName,
            players: [playerOne.username],
            score_percentage: 80,
            megaround: { round: 6, values: { '1': 1, '2': 2, '3': 3, '4': 4, '5': 5 } }
        }
    }
};

test.beforeAll(async ({ p1 }) => {
    // set up the event data
    apicontext = apicontext = await createApiContext();
    const response = await apicontext.post('ops/run-game/', {
        headers: await p1.getAuthHeader(),
        data: { game_data: JSON.stringify(game_data) }
    });
    expect(response.status()).toBe(200);
});

test.afterAll(async () => {
    apicontext.dispose();
});

test('the megaround updates properly', async ({ p1 }) => {
    await p1.page.goto('/game/7812/megaround');
    await expect(p1.page).toHaveURL('/game/7812/megaround');

    const rdSelector = p1.page.locator('div.round-selector');
    // only 2nd half rounds are available
    await expect(rdSelector.locator('button')).toHaveCount(4);
    await expect(rdSelector.locator('button').first()).toHaveText(/5/);
    await expect(rdSelector.locator('button').last()).toHaveText(/8/);

    const mrInputs = p1.page.locator('div.input-container');
    await expect(mrInputs.locator('#megaround-weight-1')).toHaveValue('1');
    await rdSelector.locator('button', { hasText: /8/ }).click();
    await expect(mrInputs.locator('#megaround-weight-1')).toBeEmpty();
    const submitBtn = p1.page.locator('button', { hasText: /submit/i });
    await expect(submitBtn).toBeDisabled();

    const mrWeightOpts = p1.page.locator('div.megaround-weight-selector');

    for (let i = 1; i <= 5; i++) {
        const btnLoc = mrWeightOpts.locator('button', { hasText: new RegExp(String(i)) });
        await expect(btnLoc).toBeVisible();
        await btnLoc.click();
        await expect(mrInputs.locator(`#megaround-weight-${i}`)).toHaveValue(String(i));
    }

    await expect(submitBtn).toBeEnabled();
    await submitBtn.click();

    // validate the we've update the selected megaround in the database
    const response = await apicontext.post('ops/validate/', {
        headers: await p1.getAuthHeader(),
        // rd 8 should be the megaround for team 1
        data: { type: 'validate_megaround', round: 8, team: playerOne.teamName, joincode: 7812 }
    });
    if (response.status() !== 200) {
        throw new Error(await response.json());
    }
});

test('a player that has not joined the game cannot submit a megaround', async ({ p3 }) => {
    await p3.page.goto('/game/7812/megaround');
    await expect(p3.page).toHaveURL('/game/7812/megaround');

    await expect(p3.page.locator('h3.not-joined-warning')).toBeVisible();
    await p3.page.locator('div.round-selector').locator('button', { hasText: /8/ }).click();
    await expect(p3.page.locator('button', { hasText: /submit/i })).toBeDisabled();
});

test('a player cannot see locked megarounds', async ({ p1 }) => {
    const response = await apicontext.post('ops/validate/', {
        headers: await p1.getAuthHeader(),
        // rd 8 should be the megaround for team 1
        data: { type: 'megaround_lock', joincode: 7812 }
    });
    expect(response.status()).toBe(200);

    await p1.page.goto('/game/7812/megaround');
    await expect(p1.page).toHaveURL('/game/7812/megaround');

    await expect(p1.page.locator('div.round-selector')).not.toBeVisible();
});
