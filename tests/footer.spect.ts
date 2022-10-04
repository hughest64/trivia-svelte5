// what footer content should be on a give page
import { expect, test } from '@playwright/test';
// import { login } from './utils.js';

// create a test hook, log in with beforeAll?

// login page - nothing
test.skip('tests should pass', async ({ page }) => {
    await page.goto('/user/login');
    await expect(page).toHaveTitle(/login/i);
    // fill in the form
    // click the button
});
// welcome page - nothing
// root - menu only (team select/host choice)
// game/join - menu only
// game/[joincode]/xxx - all (megaround, not scoring)
// host/event-setup - menu only
// host/[joincode]/xxx all (scoring, not megaround)

// click on the icons and make sure that there are no errors and the correct headers and/or urls render