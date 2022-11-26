import { expect, test } from '@playwright/test';
import { defaultQuestionText, PlayerGamePage, HostGamePage } from './gamePages.js';
import { asyncTimeout, getBrowserPage, resetEventData } from './utils.js';
import type { TestConfig } from './utils.js';

// TODO future:
// test image and sound rounds should be auto-revealed,
// this is probably part of testing event creation when we get to that

// allow some time to pass before checking question reveal states,
// it's worth noting that we use a 1 second delay for the app in test mode
// and tests here may pass without any delay
const revealDelay = 1000;

const current = /current/;

const triviaEventOne = '/game/1234';
const triviaEventTwo = '/game/9999';

const testconfigs: Record<string, TestConfig> = {
    p1: { pageUrl: triviaEventOne },
    p2: { pageUrl: triviaEventOne, username: 'player_two', password: 'player_two' },
    p3: { pageUrl: triviaEventTwo, username: 'player_three', password: 'player_three' },
    host: { pageUrl: '/host/1234', username: 'sample_admin', password: 'sample_admin' }
};

let p1: PlayerGamePage; // game 1234 w/ auto reveal
let p2: PlayerGamePage; // game 1234 no auto reveal
let p3: PlayerGamePage; // game 9999 w/ auto reveal
let host: HostGamePage; // game 1234

test.beforeEach(async ({ browser }) => {
    p1 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p1);
    p2 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p2);
    p3 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p3);
    host = new HostGamePage(await getBrowserPage(browser), testconfigs.host);
});

test.afterEach(async () => {
    await p1.logout();
    await p2.logout();
    await p3.logout();
    await host.logout();

    await resetEventData();
});

test('all players start on round one question one', async () => {
    // everyone is on the right question
    await p1.expectCorrectQuestionHeading('1.1');
    await p2.expectCorrectQuestionHeading('1.1');
    await p3.expectCorrectQuestionHeading('1.1');
    await host.expectRoundToBe('1');
});

test('active round and question classes are applied properly', async () => {
    // check for current class on 1.1
    await expect(host.roundButton('1')).toHaveClass(current);
    await expect(p1.roundButton('1')).toHaveClass(current);
    await expect(p1.questionSelector('1.1')).toHaveClass(current);

    // host got to rd 2, reveal question2
    await host.roundButton('2').click();
    await host.revealQuestion('2.1');

    // 2.1 should be current
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

test('question text reveals properly for players', async () => {
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
    await expect(p3.dismissButton).not.toBeVisible();
    await expect(host.dismissButton).toBeVisible();

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

test('auto reveal respects player settings', async () => {
    // host reveals 1.2
    await host.revealQuestion('1.2');
    await asyncTimeout(revealDelay);
    await host.expectQuestionToBeRevealed('1.2');
    await p1.expectCorrectQuestionHeading('1.2');
    await p2.expectCorrectQuestionHeading('1.1');
    await p3.expectCorrectQuestionHeading('1.1');
});

// TODO: skipping slow and flaky test
test('reveal all reveals all questions for a round', async () => {
    // host reveals all for round 2
    await host.roundButton('2').click();
    await host.expectRoundToBe('2');

    // host find and click reveal all
    await host.revealQuestion('all');

    await asyncTimeout(revealDelay);
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

test('round locks work properly', async () => {
    await expect(p1.responseInput).toBeEditable();
    await expect(p3.responseInput).toBeEditable();

    const lockIconLabel = host.lockIconLabel('1');
    await host.expectLockedIconNotToBeVisible('1');
    await lockIconLabel.click();

    await host.expectLockedIconToBeVisible('1');
    await expect(p1.responseInput).toBeDisabled();
    await expect(p3.responseInput).toBeEditable();
});

test('unlocking a round requires host confirmation', async () => {
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
