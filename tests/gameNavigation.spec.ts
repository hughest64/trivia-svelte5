import { expect, test } from './fixtures.js';
import { asyncTimeout, resetEventData } from './utils.js';

/**
 * TODO:
 * - test swiping (how to do this?)
 */

const joincode = '9901';
const submission = 'a different answer';

test.beforeEach(async () => {
    await resetEventData({ joincodes: joincode });
});

test('round question cookies work properly', async ({ p1Page }) => {
    await p1Page.joinGame(joincode);
    await p1Page.expectCorrectQuestionHeading('1.1');

    await p1Page.page.locator('.round-selector').locator('button:has-text("3")').click();
    await p1Page.expectCorrectQuestionHeading('3.1');

    const questionThree = p1Page.page.locator('.question-selector').locator('button:has-text("4")');
    await questionThree.click();
    await p1Page.expectCorrectQuestionHeading('3.4');

    await p1Page.page.reload();
    await p1Page.expectCorrectQuestionHeading('3.4');
});

test.skip('arrow keys change the active question', async ({ p1Page }) => {
    await p1Page.joinGame(joincode);
    await p1Page.expectCorrectQuestionHeading('1.1');
    await p1Page.page.keyboard.press('ArrowRight');
    await asyncTimeout(200);
    await p1Page.expectCorrectQuestionHeading('1.2');
});

test.skip('unsubmitted class is applied properly', async ({ p1Page }) => {
    await p1Page.joinGame(joincode);
    const responseInput = p1Page.page.locator('input[name="response_text"]');
    // expect the class not be to applied
    await expect(p1Page.page.locator('div#response-container')).not.toHaveClass(/notsubmitted/);

    await responseInput.fill(submission);
    await expect(p1Page.page.locator('div#response-container')).toHaveClass(/notsubmitted/);

    await p1Page.page.locator('button:has-text("Submit")').click();
    await expect(p1Page.page.locator('div#response-container')).toHaveClass(/notsubmitted/);
});

test('navigating away from the event page and back retains the active question', async ({ p1Page }) => {
    await p1Page.joinGame(joincode);
    await p1Page.expectCorrectQuestionHeading('1.1');
    await p1Page.page.locator('.question-selector').locator('id=1.3').click();
    await p1Page.expectCorrectQuestionHeading('1.3');

    // navigate to another page
    await p1Page.page.locator('p', { hasText: 'Chat' }).click();
    await p1Page.page.locator('p', { hasText: 'Quiz' }).click();
    await expect(p1Page.page.locator('h2', { hasText: 'General Knowledge' })).toBeVisible();

    // try to move again
    await p1Page.page.locator('.question-selector').locator('id=1.4').click();
    await p1Page.expectCorrectQuestionHeading('1.4');
});
