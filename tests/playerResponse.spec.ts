import { expect, test } from '@playwright/test';
import type { Page } from '@playwright/test';
import { login } from './utils.js';

/**
 * TODO: read up on multiple contexts, is a describe wrapper necessary? (I feel like not) 
 * we need three players, two on one team, one alone
 * each player
 * - log in
 * - select a team
 * - goto /game/1234
 * 
 * test player one submits a response
 * - (p1) expect the notsubmitted class to be applied before submission
 * - (p1) expcct the not submitted class to be not after submission
 * - (p2) expect the input to have updated with the response from p1
 * - (p3) excpet the input to have not updated with the response p1
 * 
 * test player 3 submits a response
 * - (p1 and p2) do not recieve the updated responzse
 */

let pOnePage: Page;
let pTwoPage: Page;
let pThreePage: Page;

// TODO: set up in before each? or maybe that's why we use test.describe and do beforeAll?
test.beforeEach(async ({ browser }) => {
    // same team
    const playerOnecontext = await browser.newContext();
    const playerTwocontext = await browser.newContext();
    // different team
    const playerThreecontext = await browser.newContext();

    // default user 'player'
    pOnePage = await playerOnecontext.newPage();
    await login(pOnePage);
    await pOnePage.goto('/game/1234');

    // TODO: anoother player, not sample_admin, cuz we can't set a default team for them
    pTwoPage = await playerTwocontext.newPage();
    await login(pTwoPage);
    await pTwoPage.goto('/game/1234');

    // TODO: guest?
    pThreePage = await playerThreecontext.newPage();
    await login(pThreePage);
    await pThreePage.goto('/game/1234');
});

test('not submitted class is applied when a response has not been submitted', async () => {
    
    await expect(pOnePage).toHaveURL('/game/1234');
    await expect(pTwoPage).toHaveURL('/game/1234');
    await expect(pThreePage).toHaveURL('/game/1234');
});


