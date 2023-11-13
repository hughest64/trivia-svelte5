import { test, expect } from '@playwright/test';
import { getUserPage } from './authConfigs.js';
import { createApiContext } from './utils.js';
import type { APIRequestContext } from '@playwright/test';
import type { HostGamePage } from './gamePages.js';

let apicontext: APIRequestContext;
let host: HostGamePage;

let joincodes: string[] = [];

test.beforeAll(async ({ browser }) => {
    host = (await getUserPage(browser, 'host')) as HostGamePage;
    apicontext = apicontext = await createApiContext();
    // update the date_used of test block games so they show up for the host
    const response = await apicontext.post('ops/game-setup/', {
        headers: await host.getAuthHeader(),
        data: {}
    });
    expect(response.status()).toBe(200);
});

test.afterEach(async () => {
    const response = await apicontext.post('ops/delete/', {
        headers: await host.getAuthHeader(),
        data: { type: 'game', joincodes }
    });
    joincodes = [];
    expect(response.status()).toBe(200);
});

test.afterAll(async () => {
    await host.page.context().close();
    await apicontext.dispose();
});

test('default selected event changes based on inputs', async () => {
    await host.page.goto('/host/event-setup');
    await expect(host.page).toHaveURL('/host/event-setup');
    await expect(host.page.locator('#location_select')).toHaveText(/happening place/i);
    // expect that the game title endswith /nosound/i
    await expect(host.page.locator('#game_select')).toHaveText(/nosound/i);

    // return;

    // choose use sound
    const soundBtn = host.page.locator('#sound-btn');
    await expect(soundBtn).toBeVisible();
    await soundBtn.click();
    // expect !endswith /nosound/i
    await expect(host.page.locator('#game_select')).not.toHaveText(/nosound/i);

    // click host event
    const submitBtn = host.page.locator('button[type="submit"]');
    await expect(submitBtn).toBeVisible();
    await submitBtn.click();
    // check the game details on the event
    const detailHeader = host.page.locator('h4', { hasText: /detail/i }).locator('strong');
    await expect(detailHeader).toHaveText(/happening place/i);
    await expect(detailHeader).not.toHaveText(/nosound/i);

    const joincodeHeader = host.page.locator('h4', { hasText: /event join code/i }).locator('strong');
    const joincode = await joincodeHeader.textContent();
    joincodes.push(joincode as string);

    // expect a player limit to not be set
    const response = await apicontext.post('ops/validate/', {
        headers: await host.getAuthHeader(),
        data: { type: 'player_limit', limit: null, joincode }
    });

    // log the response if we don't get a 200
    if (response.status() !== 200) {
        console.log(await response.json());
    }
    expect(response.status()).toBe(200);
});

test('player limit gets set properly', async () => {
    await host.page.goto('/host/event-setup');
    await expect(host.page).toHaveURL('/host/event-setup');

    const playerLimit = host.page.locator('#player-limit-btn');
    await expect(playerLimit).toBeVisible();
    await playerLimit.click();

    const submitBtn = host.page.locator('button[type="submit"]');
    await expect(submitBtn).toBeVisible();
    await submitBtn.click();

    const joincodeHeader = host.page.locator('h4', { hasText: /event join code/i }).locator('strong');
    const joincode = await joincodeHeader.textContent();
    joincodes.push(joincode as string);

    // expect a player limit to not be set
    const response = await apicontext.post('ops/validate/', {
        headers: await host.getAuthHeader(),
        data: { type: 'player_limit', limit: 1, joincode }
    });

    // log the response if we don't get a 200
    if (response.status() !== 200) {
        console.log(await response.json());
    }
    expect(response.status()).toBe(200);
});

// TODO:
// - select a new block and validate the selected game
// - validate button language for existing vs non-existing games
