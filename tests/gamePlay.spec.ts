import { expect, test } from './fixtures.js';
import { defaultQuestionText } from './gamePages.js';
import { asyncTimeout, resetEventData } from './utils.js';

// TODO future:
// test image and sound rounds should be auto-revealed,
// this is probably part of testing event creation when we get to that

// allow some time to pass before checking question reveal states,
// it's worth noting that we use a 1 second delay for the app in test mode
// and tests here may pass without any delay
const revealDelay = 1000;

const current = /current/;

const joincode_1 = '9904';
const joincode_2 = '9905';
const hostUrl = `/host/${joincode_1}`;

test.beforeEach(async () => {
    await resetEventData({ joincode: joincode_1 });
    await resetEventData({ joincode: joincode_2 });
});

test('active round and question classes are applied properly', async ({ p1Page, hostPage }) => {
    await p1Page.joinGame(joincode_1);
    await hostPage.page.goto(hostUrl);

    // check for current class on 1.1
    await expect(hostPage.roundButton('1')).toHaveClass(current);
    await expect(p1Page.roundButton('1')).toHaveClass(current);
    await expect(p1Page.questionSelector('1.1')).toHaveClass(current);

    // host got to rd 2, reveal question2
    await hostPage.roundButton('2').click();
    await hostPage.revealQuestion('2.1');

    // 2.1 should be current
    await asyncTimeout(revealDelay);
    await expect(hostPage.roundButton('2')).toHaveClass(current);
    await expect(p1Page.roundButton('2')).toHaveClass(current);
    await expect(p1Page.questionSelector('2.1')).toHaveClass(current);

    // host go back to rd 1, reveal q5
    // 1.5 should not be set as current
    await hostPage.roundButton('1').click();
    await hostPage.revealQuestion('1.5');

    await expect(hostPage.roundButton('1')).not.toHaveClass(current);

    // p1 should not be directed backwards? (not sure about this)
    await expect(p1Page.roundButton('2')).toHaveClass(current);
    await expect(p1Page.questionSelector('2.1')).toHaveClass(current);
});

test('question text reveals properly for players', async ({ p1Page, p2Page, p3Page, hostPage }) => {
    await p1Page.joinGame(joincode_1);
    await p1Page.goToQuestion('1.1');
    await p2Page.joinGame(joincode_1);
    await p2Page.goToQuestion('1.1');
    await p3Page.joinGame(joincode_2);
    await hostPage.page.goto(hostUrl);
    // check 1.1 question text
    await expect(p1Page.questionTextField('1.1')).toHaveText(defaultQuestionText);
    await expect(p2Page.questionTextField('1.1')).toHaveText(defaultQuestionText);
    await expect(p3Page.questionTextField('1.1')).toHaveText(defaultQuestionText);

    // host reveals 1.1
    await hostPage.expectQuestionToNotBeRevealed('1.1');
    await hostPage.revealQuestion('1.1');
    await hostPage.expectQuestionToBeRevealed('1.1');

    // popup should be displayed for p1 and host
    await expect(p1Page.dismissButton).toBeVisible();
    await expect(p2Page.dismissButton).toBeVisible();
    await expect(hostPage.dismissButton).toBeVisible();
    await expect(p3Page.dismissButton).not.toBeVisible();

    // check question text
    await asyncTimeout(revealDelay);
    await expect(p1Page.questionTextField('1.1')).not.toHaveText(defaultQuestionText);
    await expect(p2Page.questionTextField('1.1')).not.toHaveText(defaultQuestionText);
    await expect(p3Page.questionTextField('1.1')).toHaveText(defaultQuestionText);

    // test that the popup has closed
    await expect(p1Page.dismissButton).not.toBeVisible();
    await expect(hostPage.dismissButton).not.toBeVisible();

    // test that no api error occured that would reset the reveal status
    await hostPage.expectQuestionToBeRevealed('1.1');
});

test('auto reveal respects player settings', async ({ p1Page, p2Page, p3Page, hostPage }) => {
    await p1Page.joinGame(joincode_1);
    await p2Page.joinGame(joincode_1);
    await p3Page.joinGame(joincode_2);
    await hostPage.page.goto(hostUrl);
    // host reveals 1.2
    await hostPage.revealQuestion('1.2');
    await asyncTimeout(1500);
    await hostPage.expectQuestionToBeRevealed('1.2');
    await p1Page.expectCorrectQuestionHeading('1.2');
    await p2Page.expectCorrectQuestionHeading('1.1');
    await p3Page.expectCorrectQuestionHeading('1.1');
});

test('reveal all reveals all questions for a round', async ({ p1Page, p2Page, hostPage }) => {
    await p1Page.joinGame(joincode_1);
    await p2Page.joinGame(joincode_1);
    await hostPage.page.goto(hostUrl);
    // host reveals all for round 2
    await hostPage.roundButton('2').click();
    await hostPage.expectRoundToBe('2');

    // host find and click reveal all
    await hostPage.revealQuestion('all');

    await asyncTimeout(1500);
    await p1Page.expectCorrectQuestionHeading('2.1');
    await p2Page.expectCorrectQuestionHeading('1.1');
    await p2Page.roundButton('2').click();

    const questionNumbers = ['2.1', '2.2', '2.3', '2.4', '2.5'];
    for (const key of questionNumbers) {
        await hostPage.expectQuestionToBeRevealed(key);

        await p1Page.goToQuestion(key);
        await p2Page.goToQuestion(key);
        // NOTE: this makes this test very slow, but it's necessary
        // in order to allow the question transition to complete
        await asyncTimeout(350);

        await p1Page.expectCorrectQuestionHeading(key);
        await p1Page.expectQuestionTextNotToBeDefault(key);
        await p2Page.expectCorrectQuestionHeading(key);
        await p2Page.expectQuestionTextNotToBeDefault(key);
    }
});

test('round locks work properly', async ({ p1Page, p3Page, hostPage }) => {
    await p1Page.joinGame(joincode_1);
    await p3Page.joinGame(joincode_2);
    await hostPage.page.goto(hostUrl);
    await expect(p1Page.responseInput).toBeEditable();
    await expect(p3Page.responseInput).toBeEditable();

    const lockIconLabel = hostPage.lockIconLabel('1');
    await hostPage.expectLockedIconNotToBeVisible('1');
    await lockIconLabel.click();

    await hostPage.expectLockedIconToBeVisible('1');
    await expect(p1Page.responseInput).toBeDisabled();
    await expect(p3Page.responseInput).toBeEditable();
});

test('unlocking a round requires host confirmation', async ({ hostPage }) => {
    await hostPage.page.goto(hostUrl);
    // goto round 3
    await hostPage.roundButton('3').click();
    await hostPage.expectRoundToBe('3');

    // lock the round
    const lockIconLabel = hostPage.lockIconLabel('3');
    await hostPage.expectLockedIconNotToBeVisible('3');
    await lockIconLabel.click();
    await hostPage.expectLockedIconToBeVisible('3');

    // try to unlock the round
    await lockIconLabel.click();
    await hostPage.expectLockedIconToBeVisible('3');

    // confirm the unlock
    const btn = hostPage.page.locator('.pop-content').locator('button');
    await btn.click();
    await expect(btn).not.toBeVisible();
    await hostPage.expectLockedIconNotToBeVisible('3');
});
