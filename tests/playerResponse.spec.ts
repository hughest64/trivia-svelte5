import { expect, test } from '@playwright/test';
import type { Page } from '@playwright/test';
import { login } from './utils.js';

/**
 * TODO: * 
 * test player one submits a response
 * - (p1) expect the notsubmitted class to be applied before submission
 * - (p1) expcct the not submitted class to be not after submission
 * - (p2) expect the input to have updated with the response from p1
 * - (p3) excpet the input to have not updated with the response p1
 * 
 * test player 3 submits a response
 * - (p1 and p2) do not recieve the updated response
 * 
 * test a player connected to a different game but a differnt team
 * - ( I think this will fail right now due to how team groups are nameed)
 * 
 * not related to responses (other than loading?)
 * - click a different round
 * - expect r.q to change
 * - click a different question
 * - expect r.q to change
 * - refresh the page
 * - expect r.q to persist
 * 
 * - test arrow key for changing questions
 * - test swiping (how to do this?)
 * 
 * - test input classname change on unsubmitted response
 */

const gamePage = '/game/1234';
const submissionOne = 'answer for question';
// const submissionTwo = 'a different answer';

let playerOnePage: Page;
let playerTwoPage: Page;
let playerThreePage: Page;

test.beforeEach(async ({ browser }) => {
    // same team
    const playerOnecontext = await browser.newContext();
    const playerTwocontext = await browser.newContext();
    // different team
    const playerThreecontext = await browser.newContext();

    // default user 'player'
    playerOnePage = await playerOnecontext.newPage();
    await login(playerOnePage);
    await playerOnePage.goto(gamePage);
    await expect(playerOnePage).toHaveURL(gamePage);

    // player_two
    playerTwoPage = await playerTwocontext.newPage();
    await login(playerTwoPage, { username: 'player_two', password: 'player_two' });
    await playerTwoPage.goto(gamePage);
    await expect(playerTwoPage).toHaveURL(gamePage);

    // guest user
    playerThreePage = await playerThreecontext.newPage();
    await login(playerThreePage, { username: 'guest', password: 'guest' });
    await playerThreePage.goto(gamePage);
    await expect(playerThreePage).toHaveURL(gamePage);
});

// TODO: this isn't working as expected.
test('proper response handling', async () => {
    // all players on round one question one
    expect(await playerOnePage.textContent('h2')).toBe('1.1');
    expect(await playerTwoPage.textContent('h2')).toBe('1.1');
    expect(await playerThreePage.textContent('h2')).toBe('1.1');

    const playerOneResponseInput = playerOnePage.locator('input[name="response_text"]');
    const playerTwoResponseInput = playerTwoPage.locator('input[name="response_text"]');
    const playerThreeResponseInput = playerThreePage.locator('input[name="response_text"]');

    // all players have a blank input
    expect(await playerOneResponseInput.inputValue()).toBeFalsy();
    expect(await playerTwoResponseInput.inputValue()).toBeFalsy();
    expect(await playerThreeResponseInput.inputValue()).toBeFalsy();

    await playerOnePage.locator('input[name="response_text"]').fill(submissionOne);
    expect(await playerOneResponseInput.inputValue()).toBe(submissionOne);
    await playerOnePage.locator('button:has-text("Submit")').click();

    // response should persist
    expect(await playerOneResponseInput.inputValue()).toBe(submissionOne);

    // player two should have the same input as player one
    expect(await playerTwoResponseInput.inputValue()).toBe(submissionOne);

    // player three should not have the same input
    expect(await playerThreeResponseInput.inputValue()).toBeFalsy();

    // enter a response as player one did
    // should have the answer set
    // player one and player two should not have a changed input
});


