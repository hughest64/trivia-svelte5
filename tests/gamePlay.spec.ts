import { expect, test } from '@playwright/test';
import { PlayerGamePage } from './gamepage.js';
import type { Browser, Page } from '@playwright/test';

const triviaEventOne = '/game/1234';
// const triviaEventTwo = '/game/9999';

// credentials object?


// TODO: probably move to utils
const getBrowserPage = async (browser: Browser): Promise<Page> => {
    return browser.newContext().then((context) => context.newPage());
};

test.describe('simulate two trivia events simeltaneously', () => {
    let p1: PlayerGamePage;
    // let p2: PlayerGamePage; // same event and team as p1
    // let p3: PlayerGamePage; // same event different team as p1, p2
    // let p4: PlayerGamePage; // different event same team as p3

    test.beforeEach(async ({ browser }) => {
        p1 = new PlayerGamePage(await getBrowserPage(browser), triviaEventOne);
    });

    test.afterEach(async () => {
        await p1.logout();
    });

    test.afterAll(async () => {
        // TODO: hit the api directly to run reset manage cmd?
        // https://playwright.dev/docs/test-api-testing
    });

    // TODO: remove
    test('testing the POM', async () => {
        await expect(p1.page).toHaveURL(p1.gamePage);
        await expect(p1.questionHeading('1.1')).toHaveText('1.1');
        await p1.setResponse('test');
        // TOOD: method on the class for this
        expect(await p1.responseInput.inputValue()).toBe('test');
        await p1.setResponse('');

    });
    // copy the tests from playerResponse.spec
});

// tests for question reveal, auto reveal, round lock, etc (probably a separate file)
// will need host for game 1234, one palyer for game 1234, one palyer for game 9999
