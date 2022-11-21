import { expect, test } from '@playwright/test';
import { PlayerGamePage } from './gamePages.js';
import { asyncTimeout, getBrowserPage, resetEventData } from './utils.js';
import type { TestConfig } from './utils.js';

// TODO future:
// test image and sound rounds should be auto-revealed

const triviaEventOne = '/game/1234';
const triviaEventTwo = '/game/9999';

const testconfigs: Record<string, TestConfig> = {
    p1: { pageUrl: triviaEventOne },
    p2: { pageUrl: triviaEventTwo, username: 'player_two', password: 'player_two' },
    host: { pageUrl: triviaEventOne, username: 'sample_admin', password: 'sample_admin' }
};

let p1: PlayerGamePage;
let p2: PlayerGamePage;
// let host: HostGamePage;

test.beforeEach(async ({ browser }) => {
    p1 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p1);
    p2 = new PlayerGamePage(await getBrowserPage(browser), testconfigs.p2);
    // host = 
});

test.afterEach(async () => {
    p1.logout();
    p2.logout();
});

test.afterAll(async () => {
    await resetEventData();
});

// tests for question reveal, auto reveal, round lock, etc (probably a separate file)
// will need host for game 1234, one player for game 1234, one player for game 9999

test.skip('question text reveals properly for players', async () => {
    // everyone is on the right page and question

    // check 1.1 question text

    // host reveals 1.1
    // check question text
});

test.skip('auto reveal respects player settings', async () => {
    // host got to 1.2
    // check host is on 1.2
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