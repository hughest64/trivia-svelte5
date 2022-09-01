// what footer content should be on a give page
import { expect, test } from '@playwright/test';

// we need a login shortcut

// login page - nothing
test.skip('tests should pass', async ({ page }) => {
    await page.goto('/user/login');
    await expect(page).toHaveTitle(/login/i);
    // fill in the form
    // click the button
});
// welcome page - nothing
// root - menu only (team select/host choice)
// game/goin - menu only
// game/[joincode]/xxx - all (megaround, not scoring)
// host/event-setup - menu only
// host/[joincode]/xxx all (scoring, not megaround)