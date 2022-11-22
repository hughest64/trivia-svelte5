import { /* expect, */ expect, test } from '@playwright/test';
import { PlayerGamePage, HostGamePage } from './gamePages.js';
import { /* asyncTimeout, */ getBrowserPage, resetEventData } from './utils.js';
import type { TestConfig } from './utils.js';

// TODO future:
// test image and sound rounds should be auto-revealed

const triviaEventOne = '/game/1234';
const triviaEventTwo = '/game/9999';

const testconfigs: Record<string, TestConfig> = {
    p1: { pageUrl: triviaEventOne },
    p2: { pageUrl: triviaEventTwo, username: 'player_two', password: 'player_two' },
    host: { pageUrl: '/host/1234', username: 'sample_admin', password: 'sample_admin' }
};

let p1: PlayerGamePage;
let p2: PlayerGamePage;
let host: HostGamePage;

test.beforeEach(async ({ browser }) => {
    p1 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p1);
    p2 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p2);
    host = new HostGamePage(await getBrowserPage(browser), testconfigs.host);
});

test.afterEach(async () => {
    await p1.logout();
    await p2.logout();
    await host.logout();
});

test.afterAll(async () => {
    await resetEventData();
});

test('question text reveals properly for players', async () => {
    // everyone is on the right question
    await p1.expectCorrectQuestionHeading('1.1');
    await p2.expectCorrectQuestionHeading('1.1');
    await host.expectRoundToBe('1');

    // check 1.1 question text
    await expect(p1.questionTextField).toHaveText(p1.defaultQuestonText);
    await expect(p2.questionTextField).toHaveText(p2.defaultQuestonText);

    // host reveals 1.1
    const q = host.page.locator('label[for="1.1"]');
    await expect(q).toBeVisible();
    await expect(q.locator('.revealed')).not.toBeVisible();
    await q.locator('button').click();
    await expect(q.locator('.revealed')).toBeVisible();


    // asyncTimeout(1000) // checkout https://playwright.dev/docs/test-timeouts
    // test popup (just that it exists)
    // asyncTimeout(4000) (ick)
    // check question text
    // test that the popup has closed
});

test('auto reveal respects player settings', async () => {
    // host got to 1.2
    await host.expectRoundToBe('1');
    await host.roundButton('2').click();
    await host.expectRoundToBe('2');

    // host reveals 1.2
    // check slider for host
    // check 1.2 for all
    // current round/question classes
});

test.skip('reveal all reveals all questions for a round', async () => {
    // host reveals all for 1.1
    // check all questions for host and player (a helper or forEach seems in order here)
});

test.skip('round locks work properly', async () => {
    // host locks round 1
    // lock class should be applied for host
    // input and submit button should be disabled for player one
    // but on for player two
});
