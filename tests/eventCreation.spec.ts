import { test, expect } from '@playwright/test';
import { getUserPage } from './authConfigs.js';
import { createApiContext } from './utils.js';
import type { APIRequestContext } from '@playwright/test';
import type { HostGamePage } from './gamePages.js';

let apicontext: APIRequestContext;
let host: HostGamePage;

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

test.afterAll(async () => {
    await host.page.context().close();
    await apicontext.dispose();
});

test('host can view game options', async () => {
    await host.page.goto('/host/event-setup');
    await expect(host.page).toHaveURL('/host/event-setup');
    // expecthost home location is happening place and use sound is not checked
    await expect(host.page.locator('#location_select')).toHaveText(/happening place/i);
    // expect that the game title endswith /nosound/i
    await expect(host.page.locator('#game_select')).toHaveText(/nosound/i);

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

    // TODO api check that there is no player limit

    const response = await apicontext.post('ops/game-delete/', {
        headers: await host.getAuthHeader(),
        data: { joincodes: [joincode] }
    });
    expect(response.status()).toBe(200);
});

// NEW TEST
// goto page select
// change block (?)
// expect game to have the new name

// test player limit setting
// - check the box and post
// - use the api context to valdiate the event was created w/ a one player limit
// - add created jc to the list
