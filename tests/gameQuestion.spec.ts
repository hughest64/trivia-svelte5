import { expect, test } from '@playwright/test';
import { PlayerGamePage, HostGamePage } from './gamePages.js';
import { asyncTimeout, getBrowserPage, resetEventData } from './utils.js';
import type { TestConfig } from './utils.js';

// TODO future:
// test image and sound rounds should be auto-revealed

// allow some time to pass before checking question revale states,
// it's worth noting that we use a 2 seconds for the app in test mode
// and tests here may pass without any delay
const revealDelay = 1000;

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

// test.afterAll(async () => {
//     await resetEventData();
// });

// TODO: if we ensure we are using the env var for reveal timeout properly,
// we could set process.env here so that the reveal delay is much shorter for testing
test('question text reveals properly for players', async () => {
    // everyone is on the right question
    await p1.expectCorrectQuestionHeading('1.1');
    await p2.expectCorrectQuestionHeading('1.1');
    await p3.expectCorrectQuestionHeading('1.1');
    await host.expectRoundToBe('1');

    // check 1.1 question text
    await expect(p1.questionTextField).toHaveText(p1.defaultQuestonText);
    await expect(p2.questionTextField).toHaveText(p2.defaultQuestonText);
    await expect(p3.questionTextField).toHaveText(p3.defaultQuestonText);

    // host reveals 1.1
    await host.expectQuestionToNotBeRevealed('1.1');
    await host.revealQuestion('1.1');
    await host.expectQuestionToBeRevealed('1.1');

    // popup should be displayed for p1 and host
    await expect(p1.dismissButton).toBeVisible();
    await expect(p2.dismissButton).toBeVisible();
    await expect(p3.dismissButton).not.toBeVisible();
    await expect(host.dismissButton).toBeVisible();
    await asyncTimeout(revealDelay);

    // check question text
    await expect(p1.questionTextField).not.toHaveText(p1.defaultQuestonText);
    await expect(p2.questionTextField).not.toHaveText(p2.defaultQuestonText);
    await expect(p3.questionTextField).toHaveText(p3.defaultQuestonText);

    // test that the popup has closed
    await expect(p1.dismissButton).not.toBeVisible();
    await expect(host.dismissButton).not.toBeVisible();

    // test that no api error occured that would reset the reveal status
    await host.expectQuestionToBeRevealed('1.1');
});

test('auto reveal respects player settings', async () => {
    // host got to 1.2
    await host.expectRoundToBe('1');

    // both players should be on 1.1
    await p1.expectCorrectQuestionHeading('1.1');
    await p2.expectCorrectQuestionHeading('1.1');
    // await p3.expectCorrectQuestionHeading('1.1');

    // host reveals 1.2
    await host.revealQuestion('1.2');
    await asyncTimeout(revealDelay);
    await host.expectQuestionToBeRevealed('1.2');
    await p1.expectCorrectQuestionHeading('1.2');
    await p2.expectCorrectQuestionHeading('1.1');
    // await p3.expectCorrectQuestionHeading('1.1');

    // TODO: current round/question classes (separate test?)
});

test('reveal all reveals all questions for a round', async () => {
    // everyone is on the right question
    await p1.expectCorrectQuestionHeading('1.1');
    await p2.expectCorrectQuestionHeading('1.1');
    await p3.expectCorrectQuestionHeading('1.1');
    await host.expectRoundToBe('1');

    // host reveals all for round 2
    await host.roundButton('2').click();
    await host.expectRoundToBe('2');

    // check all questions for host and player (a helper or forEach seems in order here)
});

test.skip('round locks work properly', async () => {
    // host locks round 1
    // lock class should be applied for host
    // input and submit button should be disabled for player one
    // but on for player two
});
