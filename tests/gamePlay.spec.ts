import { expect, test } from './authConfigs.js';
import { defaultQuestionText } from './gamePages.js';
import { asyncTimeout /* resetEventData */ } from './utils.js';

// allow some time to pass before checking question reveal states,
// it's worth noting that we use a 1 second delay for the app in test mode
// and tests here may pass without any delay
const revealDelay = 1000;

const current = /current/;

const joincode_1 = '9904';
const joincode_2 = '9905';
const hostUrl = `/host/${joincode_1}`;

// test.beforeEach(async () => {
//     await resetEventData({ joincodes: [joincode_1, joincode_2] });
// });

test.skip('active round and question classes are applied properly', async ({ p1, host }) => {
    await p1.joinGame(joincode_1);
    await host.page.goto(hostUrl);

    // check for current class on 1.1
    await expect(host.roundButton('1')).toHaveClass(current);
    await expect(p1.roundButton('1')).toHaveClass(current);
    await expect(p1.questionSelector('1.1')).toHaveClass(current);

    // host got to rd 2, reveal question2
    await host.roundButton('2').click();
    await host.revealQuestion('2.1');

    // 2.1 should be current
    await asyncTimeout(revealDelay);
    await expect(host.roundButton('2')).toHaveClass(current);
    await expect(p1.roundButton('2')).toHaveClass(current);
    await expect(p1.questionSelector('2.1')).toHaveClass(current);

    // host go back to rd 1, reveal q5
    // 1.5 should not be set as current
    await host.roundButton('1').click();
    await host.revealQuestion('1.5');

    await expect(host.roundButton('1')).not.toHaveClass(current);

    // p1 should not be directed backwards? (not sure about this)
    await expect(p1.roundButton('2')).toHaveClass(current);
    await expect(p1.questionSelector('2.1')).toHaveClass(current);
});

test.skip('question text reveals properly for players', async ({ p1, p2, p3, host }) => {
    await p1.joinGame(joincode_1);
    await p1.goToQuestion('1.1');
    await p2.joinGame(joincode_1);
    await p2.goToQuestion('1.1');
    await p3.joinGame(joincode_2);
    await host.page.goto(hostUrl);
    // check 1.1 question text
    await expect(p1.questionTextField('1.1')).toHaveText(defaultQuestionText);
    await expect(p2.questionTextField('1.1')).toHaveText(defaultQuestionText);
    await expect(p3.questionTextField('1.1')).toHaveText(defaultQuestionText);

    // host reveals 1.1
    await host.expectQuestionToNotBeRevealed('1.1');
    await host.revealQuestion('1.1');
    await host.expectQuestionToBeRevealed('1.1');

    // popup should be displayed for p1 and host
    await expect(p1.dismissButton).toBeVisible();
    await expect(p2.dismissButton).toBeVisible();
    await expect(host.dismissButton).toBeVisible();
    await expect(p3.dismissButton).not.toBeVisible();

    // check question text
    await asyncTimeout(revealDelay);
    await expect(p1.questionTextField('1.1')).not.toHaveText(defaultQuestionText);
    await expect(p2.questionTextField('1.1')).not.toHaveText(defaultQuestionText);
    await expect(p3.questionTextField('1.1')).toHaveText(defaultQuestionText);

    // test that the popup has closed
    await expect(p1.dismissButton).not.toBeVisible();
    await expect(host.dismissButton).not.toBeVisible();

    // test that no api error occured that would reset the reveal status
    await host.expectQuestionToBeRevealed('1.1');
});

test.skip('auto reveal respects player settings', async ({ p1, p2, p3, host }) => {
    await p1.joinGame(joincode_1);
    await p2.joinGame(joincode_1);
    await p3.joinGame(joincode_2);
    await host.page.goto(hostUrl);
    // host reveals 1.2
    await host.revealQuestion('1.2');
    await asyncTimeout(1500);
    await host.expectQuestionToBeRevealed('1.2');
    await p1.expectCorrectQuestionHeading('1.2');
    await p2.expectCorrectQuestionHeading('1.1');
    await p3.expectCorrectQuestionHeading('1.1');
});

test.skip('reveal all reveals all questions for a round', async ({ p1, p2, host }) => {
    await p1.joinGame(joincode_1);
    await p2.joinGame(joincode_1);
    await host.page.goto(hostUrl);
    // host reveals all for round 2
    await host.roundButton('2').click();
    await host.expectRoundToBe('2');

    // host find and click reveal all
    await host.revealQuestion('all');

    await asyncTimeout(1500);
    await p1.expectCorrectQuestionHeading('2.1');
    await p2.expectCorrectQuestionHeading('1.1');
    await p2.roundButton('2').click();

    const questionNumbers = ['2.1', '2.2', '2.3', '2.4', '2.5'];
    for (const key of questionNumbers) {
        await host.expectQuestionToBeRevealed(key);

        await p1.goToQuestion(key);
        await p2.goToQuestion(key);
        // NOTE: this makes this test very slow, but it's necessary
        // in order to allow the question transition to complete
        await asyncTimeout(350);

        await p1.expectCorrectQuestionHeading(key);
        await p1.expectQuestionTextNotToBeDefault(key);
        await p2.expectCorrectQuestionHeading(key);
        await p2.expectQuestionTextNotToBeDefault(key);
    }
});

test.skip('round locks work properly', async ({ p1, p3, host }) => {
    await p1.joinGame(joincode_1);
    await p3.joinGame(joincode_2);
    await host.page.goto(hostUrl);
    await expect(p1.responseInput).toBeEditable();
    await expect(p3.responseInput).toBeEditable();

    const lockIconLabel = host.lockIconLabel('1');
    await host.expectLockedIconNotToBeVisible('1');
    await lockIconLabel.click();

    await host.expectLockedIconToBeVisible('1');
    await expect(p1.responseInput).toBeDisabled();
    await expect(p3.responseInput).toBeEditable();
});

test.skip('unlocking a round requires host confirmation', async ({ host }) => {
    await host.page.goto(hostUrl);
    // goto round 3
    await host.roundButton('3').click();
    await host.expectRoundToBe('3');

    // lock the round
    const lockIconLabel = host.lockIconLabel('3');
    await host.expectLockedIconNotToBeVisible('3');
    await lockIconLabel.click();
    await host.expectLockedIconToBeVisible('3');

    // try to unlock the round
    await lockIconLabel.click();
    await host.expectLockedIconToBeVisible('3');

    // confirm the unlock
    const btn = host.page.locator('.pop-content').locator('button');
    await btn.click();
    await expect(btn).not.toBeVisible();
    await host.expectLockedIconNotToBeVisible('3');
});
