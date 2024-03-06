import { expect, test } from '@playwright/test';
import { asyncTimeout, locations, getUserPage, triva_events, userAuthConfigs } from './config.js';

// test venue selection (players default, etc)
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
