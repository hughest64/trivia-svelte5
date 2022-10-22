import { expect, test } from '@playwright/test';
import type { Page } from '@playwright/test';
import { asyncTimeout, login } from './utils.js';

/**
 * TODO:
 * test a player connected to a different game but a differnt team
 * - ( I think this will fail right now due to how team groups are nameed)
 * - test swiping (how to do this?)
 */

const gamePage = '/game/1234';
const submissionOne = 'answer for question';
const submissionTwo = 'a different answer';

test.describe('proper response handling during an event', async () => {
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

    test.afterEach(async () => {
        await playerOnePage.goto('/user/logout');
        await playerTwoPage.goto('/user/logout');
        await playerThreePage.goto('/user/logout');
    });

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

        await playerOneResponseInput.fill(submissionOne);
        expect(await playerOneResponseInput.inputValue()).toBe(submissionOne);
        await playerOnePage.locator('button:has-text("Submit")').click();

        // wait for the socket message
        await asyncTimeout();

        // response should persist
        expect(await playerOneResponseInput.inputValue()).toBe(submissionOne);

        // player two should have the same input as player one
        expect(await playerTwoResponseInput.inputValue()).toBe(submissionOne);

        // player three should not have the same input
        expect(await playerThreeResponseInput.inputValue()).toBeFalsy();

        // enter a response as player one did
        await playerThreeResponseInput.fill(submissionTwo);
        await playerThreePage.locator('button:has-text("Submit")').click();
        expect(await playerThreeResponseInput.inputValue()).toBe(submissionTwo);
        expect(await playerOneResponseInput.inputValue()).toBe(submissionOne);
        expect(await playerTwoResponseInput.inputValue()).toBe(submissionOne);
    });
});

test.beforeEach(async ({ page }) => {
    await login(page);
    await page.goto(gamePage);
});

test.afterEach(async ({ page }) => {
    await page.goto('/user/logout');
});

test('round question cookies work properly', async({ page }) => {
    expect(await page.textContent('h2')).toBe('1.1');

    await page.locator('.round-selector').locator('button:has-text("3")').click();
    expect(await page.textContent('h2')).toBe('3.1');

    const questionThree = page.locator('.question-selector').locator('button:has-text("4")');
    await questionThree.click();
    await asyncTimeout();
    expect(await page.textContent('h2')).toBe('3.4');

    await page.reload();
    expect(await page.textContent('h2')).toBe('3.4');
    
});

test('arrow keys change the active question', async ({ page }) => {
    expect(await page.textContent('h2')).toBe('1.1');
    await page.keyboard.press('ArrowRight');
    await asyncTimeout(150);
    expect(await page.textContent('h2')).toBe('1.2');
});

test('unsubmitted clss is applied properly', async ({ page }) => {
    const responseInput = page.locator('input[name="response_text"]');
    // expect the class not be to applied
    expect (await responseInput.inputValue()).toBeFalsy();
    await expect(page.locator('div.notsubmitted')).not.toBeVisible();
    await responseInput.fill(submissionTwo);
    // expect the class to be applied
    await expect(page.locator('div.notsubmitted')).toBeVisible();
    
    await page.locator('button:has-text("Submit")').click();
    // delay?
    // expet the class not to be applied
    await expect(page.locator('div.notsubmitted')).not.toBeVisible();
});