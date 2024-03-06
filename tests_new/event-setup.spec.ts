import { expect, test } from '@playwright/test';
import { locations, getUserPage, userAuthConfigs } from './config.js';

/**
 * TODO:
 * - test for recent events link
 * - test for creating a single device event
 *   (we don't currently have a ui way to know if an event is single device)
 */

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

test('a host can create an event', async ({ browser }) => {
    const page = await getUserPage(browser, 'host_user');
    await page.goto('/host/event-setup');

    const selectedGame = (await page.locator('p#selected-game').textContent()) as string;
    await page.locator('button', { hasText: /begin trivia/i }).click({ timeout: 5000 });
    await expect(page).toHaveURL(/host\/\d+/);
    // the selected game is the game created
    await expect(page.locator('#event-details')).toHaveText(new RegExp(selectedGame));

    // TODO: just hitting back doesn't change the button text (we haven't received updated data from the api)
    // is htat problematic?
    // the button should now say "join"
    await page.goBack();
    await page.reload();
    await expect(page.locator('button', { hasText: /join trivia/i })).toBeVisible();
});
