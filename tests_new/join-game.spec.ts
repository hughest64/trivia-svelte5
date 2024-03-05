import { expect, test } from '@playwright/test';
import { getUserPage } from './config.js';

test.skip('two players cannot join an event with a player limit', async ({ browser }) => {
    const p1 = getUserPage(browser, 'player_one');
    const p2 = getUserPage(browser, 'player_two');

    // p1 joins game 1111
    // - success
    // p2 (same team) tries to join the game
    // - gets error message - test navigation from the error?
});
