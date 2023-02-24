import { test } from './fixtures.js';
import { asyncTimeout, resetEventData } from './utils.js';

const submissionOne = 'answer for question';
const submissionTwo = 'a different answer';

test.afterAll(async () => {
    await resetEventData();
});

test('responses only update for the same team on the same event', async ({ p1Page, p2Page, p3Page, p4Page }) => {
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
