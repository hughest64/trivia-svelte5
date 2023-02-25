import { test } from '@playwright/test';
import { PlayerGamePage } from './gamePages.js';
import { asyncTimeout, resetEventData } from './utils.js';

const submissionOne = 'answer for question';
const submissionTwo = 'a different answer';

let p1Page: PlayerGamePage;
let p2Page: PlayerGamePage;
let p3Page: PlayerGamePage;
let p4Page: PlayerGamePage;

// maybe just take these steps either as a method or in the constructor of the page class?
test.beforeAll(async ({ browser }) => {
    const p1Context = await browser.newContext({ storageState: 'authStorage.playerFile' });
    p1Page = new PlayerGamePage(await p1Context.newPage());
    const p2Context = await browser.newContext({ storageState: 'authStorage.playerTwoFile' });
    p2Page = new PlayerGamePage(await p2Context.newPage());
    const p3Context = await browser.newContext({ storageState: 'authStorage.playerThreeFile' });
    p3Page = new PlayerGamePage(await p3Context.newPage());
    const p4Context = await browser.newContext({ storageState: 'authStorage.playerFourFile' });
    p4Page = new PlayerGamePage(await p4Context.newPage());
});

test.afterAll(async () => {
    await resetEventData();
});

test('responses only update for the same team on the same event', async () => {
    p1Page.joinGame('1234');
    p2Page.joinGame('1234');
    p3Page.joinGame('1234');
    p4Page.joinGame('9999');
    // everyone on the correct page/question
    await p1Page.expectCorrectQuestionHeading('1.1');
    await p2Page.expectCorrectQuestionHeading('1.1');
    await p3Page.expectCorrectQuestionHeading('1.1');
    await p4Page.expectCorrectQuestionHeading('1.1');

    // no answers filled in for 1.1
    await p1Page.expectInputValueToBeFalsy();
    await p2Page.expectInputValueToBeFalsy();
    await p3Page.expectInputValueToBeFalsy();
    await p4Page.expectInputValueToBeFalsy();

    // player one submits a response
    await p1Page.setResponse(submissionOne, { submit: true });
    await asyncTimeout(200);
    await p1Page.expectInputValueToBe(submissionOne);
    await p2Page.expectInputValueToBe(submissionOne);
    await p3Page.expectInputValueToBeFalsy();
    await p4Page.expectInputValueToBeFalsy();

    // player 4 submits a response
    await p4Page.setResponse(submissionTwo, { submit: true });
    await asyncTimeout(200);
    await p1Page.expectInputValueToBe(submissionOne);
    await p2Page.expectInputValueToBe(submissionOne);
    await p3Page.expectInputValueToBeFalsy();
    await p4Page.expectInputValueToBe(submissionTwo);
});
