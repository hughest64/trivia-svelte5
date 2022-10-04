import { expect, test } from '@playwright/test';
import { login } from './utils.js';
import type { Page } from '@playwright/test';

test.describe.skip('footer links display and navigate correctly', async () => {
    let page: Page;
    test.beforeAll(async () => {
        await login(page);
    });
    // root - no menu
    // team - menu only 
    // game/join - menu only
    // game/[joincode]/xxx - all player (megaround, not scoring)
    // once on game page, click links and ensure correct url
});

// host/event-setup - menu only
// host/[joincode]/xxx all (scoring, not megaround)