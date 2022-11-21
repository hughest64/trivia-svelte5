import { test } from '@playwright/test';
import { PlayerGamePage } from './gamePages.js';
import { asyncTimeout, getBrowserPage, resetEventData } from './utils.js';
import type { TestConfig } from './utils.js';

const triviaEventOne = '/game/1234';
const triviaEventTwo = '/game/9999';

const submissionOne = 'answer for question';
const submissionTwo = 'a different answer';

const testconfigs: Record<string, TestConfig> = {
    p1: { pageUrl: triviaEventOne },
    p2: { pageUrl: triviaEventOne, username: 'player_two', password: 'player_two' },
    p3: { pageUrl: triviaEventOne, username: 'player_three', password: 'player_three' },
    p4: { pageUrl: triviaEventTwo, username: 'player_four', password: 'player_four' }
};

let p1: PlayerGamePage; // same event and teams as p2
let p2: PlayerGamePage; // same event and team as p1
let p3: PlayerGamePage; // same event different team as p1, p2
let p4: PlayerGamePage; // different event same team as p3

test.beforeEach(async ({ browser }) => {
    p1 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p1);
    p2 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p2);
    p3 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p3);
    p4 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p4);
});

test.afterEach(async () => {
    await p1.logout();
    await p2.logout();
    await p3.logout();
    await p4.logout();
});

test.afterAll(async () => {
    await resetEventData();
});

test('responses only update for the same team on the same event', async () => {
    // everyone on the correct page/question
    await p1.expectCorrectQuestionHeading('1.1');
    await p2.expectCorrectQuestionHeading('1.1');
    await p3.expectCorrectQuestionHeading('1.1');
    await p4.expectCorrectQuestionHeading('1.1');

    // no answers filled in for 1.1
    await p1.expectInputValueToBeFalsy();
    await p2.expectInputValueToBeFalsy();
    await p3.expectInputValueToBeFalsy();
    await p4.expectInputValueToBeFalsy();

    // player one submits a response
    await p1.setResponse(submissionOne, { submit: true });
    await asyncTimeout(200);
    await p1.expectInputValueToBe(submissionOne);
    await p2.expectInputValueToBe(submissionOne);
    await p3.expectInputValueToBeFalsy();
    await p4.expectInputValueToBeFalsy();

    // player 4 submits a response
    await p4.setResponse(submissionTwo, { submit: true });
    await asyncTimeout(200);
    await p1.expectInputValueToBe(submissionOne);
    await p2.expectInputValueToBe(submissionOne);
    await p3.expectInputValueToBeFalsy();
    await p4.expectInputValueToBe(submissionTwo);
});
