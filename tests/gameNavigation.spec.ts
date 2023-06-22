import { expect, test } from './authConfigs.js';
import { asyncTimeout, createApiContext } from './utils.js';
import type { APIRequestContext } from '@playwright/test';

const joincode = '9901';
const gameUrl = '/game/' + joincode;

let apicontext: APIRequestContext;

const game_data = {
    joincode
};

test.beforeAll(async () => {
    apicontext = await createApiContext();
});

test.beforeEach(async ({ p1 }) => {
    const response = await apicontext.post('ops/run-game/', {
        headers: await p1.getAuthHeader(),
        data: { game_data: JSON.stringify(game_data) }
    });
    expect(response.status()).toBe(200);
});

test.afterAll(async ({ p1 }) => {
    await p1.page.context().close();
    await apicontext.dispose();
});

test('round question cookies work properly', async ({ p1 }) => {
    await p1.page.goto(gameUrl);
    await p1.expectCorrectQuestionHeading('1.1');

    await p1.roundSelector('3').click();
    await p1.expectCorrectQuestionHeading('3.1');

    await p1.goToQuestion('3.4');
    await p1.expectCorrectQuestionHeading('3.4');

    await p1.page.reload();
    await p1.expectCorrectQuestionHeading('3.4');
});

test('arrow keys change the active question', async ({ p1 }) => {
    await p1.page.goto(gameUrl);
    await p1.goToQuestionFromKey('1.1');

    await p1.expectCorrectQuestionHeading('1.1');
    await p1.page.keyboard.press('ArrowRight');
    await asyncTimeout(200);
    await p1.expectCorrectQuestionHeading('1.2');
});

test('navigating away from the event page and back retains the active question', async ({ p1 }) => {
    await p1.page.goto(gameUrl);
    await p1.goToQuestionFromKey('1.3');
    await p1.expectCorrectQuestionHeading('1.3');

    // navigate to another page
    await p1.page.locator('p', { hasText: 'Chat' }).click();
    await p1.page.locator('p', { hasText: 'Quiz' }).click();
    await expect(p1.page.locator('h2', { hasText: 'General Knowledge' })).toBeVisible();

    // try to move again
    await p1.page.locator('.question-selector').locator('id=1.4').click();
    await p1.expectCorrectQuestionHeading('1.4');
});
