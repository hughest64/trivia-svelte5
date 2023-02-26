import { test, expect } from './fixtures.js';
import { resetEventData } from './utils.js';

const joincode = '9900';
const eventUrl = `/game/${joincode}`;
const leaderboardUrl = `${eventUrl}/leaderboard`;

test.beforeEach(async () => {
    await resetEventData({ joincode });
});

test('player one leaderboard updates when another team joins', async ({ p1Page, p3Page }) => {
    await p1Page.joinGame(joincode);
    await p1Page.page.goto(leaderboardUrl);
    await expect(p1Page.page).toHaveURL(leaderboardUrl);

    // expect player 1's team to be on the leaderboard, but not p3
    await expect(p1Page.page.locator('h3.team-name', { hasText: /hello world/i })).toBeVisible();
    await expect(p1Page.page.locator('h3.team-name', { hasText: /for all the marbles/i })).not.toBeVisible();

    // p3 joins the game
    await p3Page.joinGame(joincode);
    await p3Page.page.goto(leaderboardUrl);

    // player 1 should now see player 3's team
    await expect(p1Page.page.locator('h3.team-name', { hasText: /for all the marbles/i })).toBeVisible();

    // player 3 should see both teams
    await expect(p3Page.page.locator('h3.team-name', { hasText: /hello world/i })).toBeVisible();
    await expect(p3Page.page.locator('h3.team-name', { hasText: /for all the marbles/i })).toBeVisible();
});

test('round headers on the leaderboard navigate back to the game', async ({ p1Page }) => {
    await p1Page.joinGame(joincode);
    await p1Page.page.goto(leaderboardUrl);
    await expect(p1Page.page).toHaveURL(leaderboardUrl);
    // click on round 5
    const rd5 = p1Page.page.locator('.round-selector').locator('button', { hasText: '5' });
    await rd5.click();
    // expect to be back on the game and round 5 is active
    await expect(p1Page.page).toHaveURL(eventUrl);
    await expect(rd5).toHaveClass('active');
});

// TODO: test actual leaderboard updates (pts values) from the host, maybe tiebreakers here too

/**
 * TODO: ideally, move all of these below back to their natural habitat
 */

// tests from gameNavigation.spec
// const submission = 'a different answer';

// test('round question cookies work properly', async ({ p1Page }) => {
//     await p1Page.joinGame('1234');
//     await p1Page.expectCorrectQuestionHeading('1.1');

//     await p1Page.page.locator('.round-selector').locator('button:has-text("3")').click();
//     await p1Page.expectCorrectQuestionHeading('3.1');

//     const questionThree = p1Page.page.locator('.question-selector').locator('button:has-text("4")');
//     await questionThree.click();
//     await p1Page.expectCorrectQuestionHeading('3.4');

//     await p1Page.page.reload();
//     await p1Page.expectCorrectQuestionHeading('3.4');
// });

// test('arrow keys change the active question', async ({ p1Page }) => {
//     await p1Page.joinGame('1234');
//     await p1Page.expectCorrectQuestionHeading('1.1');
//     await p1Page.page.keyboard.press('ArrowRight');
//     await p1Page.expectCorrectQuestionHeading('1.2');
// });

// test('unsubmitted class is applied properly', async ({ p1Page }) => {
//     await p1Page.joinGame('1234');
//     const responseInput = p1Page.page.locator('input[name="response_text"]');
//     // expect the class not be to applied
//     await expect(p1Page.page.locator('div#response-container')).not.toHaveClass(/notsubmitted/);

//     await responseInput.fill(submission);
//     await expect(p1Page.page.locator('div#response-container')).toHaveClass(/notsubmitted/);

//     await p1Page.page.locator('button:has-text("Submit")').click();
//     await expect(p1Page.page.locator('div#response-container')).toHaveClass(/notsubmitted/);
// });

// test('navigating away from the event page and back retains the active question', async ({ p1Page }) => {
//     await p1Page.joinGame('1234');
//     await p1Page.expectCorrectQuestionHeading('1.1');
//     await p1Page.page.locator('.question-selector').locator('id=1.3').click();
//     await p1Page.expectCorrectQuestionHeading('1.3');

//     // navigate to another page
//     await p1Page.page.locator('p', { hasText: 'Chat' }).click();
//     await p1Page.page.locator('p', { hasText: 'Quiz' }).click();
//     await expect(p1Page.page.locator('h2', { hasText: 'General Knowledge' })).toBeVisible();

//     // try to move again
//     await p1Page.page.locator('.question-selector').locator('id=1.4').click();
//     await p1Page.expectCorrectQuestionHeading('1.4');
// });

// // test from gameResponse .spec (this one could live alongside others but probably not here)
// const submissionOne = 'answer for question';
// const submissionTwo = 'a different answer';

// test('responses only update for the same team on the same event', async ({ p1Page, p2Page, p3Page, p4Page }) => {
//     p1Page.joinGame('1234');
//     p2Page.joinGame('1234');
//     p3Page.joinGame('1234');
//     p4Page.joinGame('9999');
//     // everyone on the correct page/question
//     await p1Page.expectCorrectQuestionHeading('1.1');
//     await p2Page.expectCorrectQuestionHeading('1.1');
//     await p3Page.expectCorrectQuestionHeading('1.1');
//     await p4Page.expectCorrectQuestionHeading('1.1');

//     // no answers filled in for 1.1
//     await p1Page.expectInputValueToBeFalsy();
//     await p2Page.expectInputValueToBeFalsy();
//     await p3Page.expectInputValueToBeFalsy();
//     await p4Page.expectInputValueToBeFalsy();

//     // player one submits a response
//     await p1Page.setResponse(submissionOne, { submit: true });
//     await asyncTimeout(200);
//     await p1Page.expectInputValueToBe(submissionOne);
//     await p2Page.expectInputValueToBe(submissionOne);
//     await p3Page.expectInputValueToBeFalsy();
//     await p4Page.expectInputValueToBeFalsy();

//     // player 4 submits a response
//     await p4Page.setResponse(submissionTwo, { submit: true });
//     await asyncTimeout(200);
//     await p1Page.expectInputValueToBe(submissionOne);
//     await p2Page.expectInputValueToBe(submissionOne);
//     await p3Page.expectInputValueToBeFalsy();
//     await p4Page.expectInputValueToBe(submissionTwo);
// });
