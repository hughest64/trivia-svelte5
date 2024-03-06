import { expect, test } from '@playwright/test';
import { asyncTimeout, locations, getUserPage, triva_events, userAuthConfigs } from './config.js';

test("a host's home lcoation is the default selection", async ({ browser }) => {
    const userData = userAuthConfigs.host_user;
    const homeLocation = locations[userData.home_location_index as number];
    const useSound = homeLocation.use_sound;
    const activeLocationCount = locations.filter((loc) => loc.active).length;
    const page = await getUserPage(browser, 'host_user');

    await page.goto('/host/event-setup');

    const locationOptions = page.locator('select#location_select').locator('option');
    const soundBtn = page.locator('button#sound-btn');

    // we have all of the active locations
    await expect(locationOptions).toHaveCount(activeLocationCount);

    // test that the first option is the host's home location
    await expect(locationOptions.first()).toHaveText(homeLocation.name);

    // test that use sound matches the location option
    if (useSound) {
        await expect(soundBtn).toHaveClass(/revealed/);
    } else {
        await expect(soundBtn).not.toHaveClass(/revealed/);
    }
});

// NOTE: game data is auto-loaded by the api and contains blocks A, B, C, and one theme night.
test('host setup options', async ({ browser }) => {
    const blocks = ['A', 'B', 'C'];
    const page = await getUserPage(browser, 'host_user');
    await page.goto('/host/event-setup');

    // theme night should not be selected
    const themeNightBtn = page.locator('button#event-type-btn');
    await expect(themeNightBtn).not.toHaveClass(/revealed/);
    // we should have a, b, c, blocks
    // a block should be selected
    const blockSelect = page.locator('select#block-select');
    const blockSelectOptions = blockSelect.locator('option');
    await expect(blockSelectOptions).toHaveCount(blocks.length);
    blocks.forEach(async (letter, i) => {
        await expect(blockSelectOptions.nth(i)).toHaveText(letter);
    });
    // game A - sound (match host pref?) should be selected
    const selectedGame = page.locator('p#selected-game');
    // await expect(selectedGame).toBeVisible();
    // NOTE: this host relies on the host having a no sound location defaulted
    await expect(selectedGame).toHaveText(/A - xNoSound/);
    await blockSelect.selectOption('B');
    await expect(selectedGame).toHaveText(/B - xNoSound/);

    // select theme night
    await themeNightBtn.click({ timeout: 5000 });
    // only one theme blcok
    await expect(blockSelectOptions).toHaveCount(1);
});
