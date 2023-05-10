import { test, request, expect } from '@playwright/test';
import type { APIRequestContext } from '@playwright/test';
import { PlayerGamePage } from './gamePages.js';

// TODO: I think it would be better to be aple to post some json instead of a filename for event setup
// this would require mods to the game runner, but keeps the data more clear and tied to this test

const api_port = process.env.API_PORT || '7000';

test.describe('proper megaround handling', async () => {
    let apicontext: APIRequestContext;

    test.beforeAll(async () => {
        apicontext = await request.newContext({
            baseURL: `http://localhost:${api_port}`
        });
        const response = await apicontext.post('/run-game', {
            headers: { 'content-type': 'application/json', accept: 'application/json' },
            data: { secret: 'todd is great', config_name: 'sample.json' }
        });
        expect(response.status()).toBe(200);
        // bodyData = await response.body();
    });
    test.afterAll(() => apicontext.dispose());

    test('the megaround updates properly', async ({ page }) => {
        const rgTeam2 = new PlayerGamePage(page);
        await rgTeam2.login('run_game_user_1', '12345');
        await rgTeam2.page.goto('/game/7812/megaround');
        await expect(rgTeam2.page).toHaveURL('/game/7812/megaround');

        const rdSelector = rgTeam2.page.locator('div.round-selector');
        // only 2nd half rounds are available
        await expect(rdSelector.locator('button')).toHaveCount(4);
        await expect(rdSelector.locator('button').first()).toHaveText(/5/);
        await expect(rdSelector.locator('button').last()).toHaveText(/8/);

        const mrInputs = rgTeam2.page.locator('div.input-container');
        await expect(mrInputs.locator('#megaround-weight-1')).toHaveValue('1');
        await rdSelector.locator('button', { hasText: /8/ }).click();
        await expect(mrInputs.locator('#megaround-weight-1')).toBeEmpty();
        const submitBtn = rgTeam2.page.locator('button', { hasText: /submit/i });
        await expect(submitBtn).toBeDisabled();

        const mrWeightOpts = rgTeam2.page.locator('div.megaround-weight-selector');

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

    // another test could lock some rounds and then the player shouldn'd be able to see them
    // hit the api first, then have the player join the game
});
