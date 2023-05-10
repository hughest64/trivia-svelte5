import { test, request, expect } from '@playwright/test';
import type { APIRequestContext } from '@playwright/test';
// import { resetEventData } from './utils.js';
import { PlayerGamePage } from './gamePages.js';

const api_port = process.env.API_PORT || '7000';

/**
 * TODO: use config but don't set a mr, and just one team
 * let the test set it and go from there
 * host should lock things in a separate api call
 */

test.describe('proper megaround handling', async () => {
    let apicontext: APIRequestContext;
    // let bodyData: Buffer;

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

    test('A players selected megaround is initially visible', async ({ page }) => {
        const rgTeam2 = new PlayerGamePage(page);
        await rgTeam2.login();
        await rgTeam2.page.goto('/game/7812/megaround');
        await expect(rgTeam2.page).toHaveURL('/game/7812/megaround');

        const rdSelector = rgTeam2.page.locator('div.round-selector');
        // only 2nd half rounds are available
        await expect(rdSelector.locator('button')).toHaveCount(4);
        await expect(rdSelector.locator('button').first()).toHaveText(/5/);
        await expect(rdSelector.locator('button').last()).toHaveText(/8/);

        await expect(rgTeam2.page.locator('h3', { hasText: /select a mega round/i })).toBeVisible();
        // go to 7
        await rdSelector.locator('button', { hasText: /7/ }).click();

        // submit button is disabled
        const submitBtn = rgTeam2.page.locator('button', { hasText: /submit/i });
        await expect(submitBtn).toBeDisabled();

        // fill the form
        const mrInputs = rgTeam2.page.locator('div.input-container');
        const mrWeightOpts = rgTeam2.page.locator('div.megaround-weight-selector');

        for (let i = 1; i <= 5; i++) {
            const btnLoc = mrWeightOpts.locator('button', { hasText: new RegExp(String(i)) });
            await expect(btnLoc).toBeVisible();
            await btnLoc.click();
            await expect(mrInputs.locator(`#megaround-weight-${i}`)).toHaveValue(String(i));
        }
        // submit
        await expect(submitBtn).toBeEnabled();
        await submitBtn.click();

        // await rgTeam2.page.reload();
        // await expect(mrInputs.locator('#megaround-weight-1')).toHaveValue('1');

        // change rd
        // form is empty
        // refresh
        // should be on 7 and form filled in
        // click the selector buttons
        // clear mr
        // form is empty
        // submit disabled

        // lock the rounds
        // await apicontext.post('/run-game', {
        //     headers: { 'content-type': 'application/json', accept: 'application/json' },
        //     data: { secret: 'todd is great', data: { joincode: 7812, lock_rounds: true } }
        // });
    });

    // maybe lock a round or two as the host and make sure p1 cannot see the round?

    /**
     * Tests:
     * - submit and refresh shows the selected mr values
     * - selected megaround text appears when on a non-mr ??
     * - final point total reflects mr values applied
     */
});
