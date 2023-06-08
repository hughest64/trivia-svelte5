import { expect, test } from '@playwright/test';
import { asyncTimeout, createApiContext } from './utils.js';
import { getUserPage } from './authConfigs.js';
import type { APIRequestContext } from '@playwright/test';
import type { PlayerGamePage } from './gamePages.js';

const joincode = '9901';
const gameUrl = '/game/' + joincode;

let apicontext: APIRequestContext;
let p1: PlayerGamePage;

const game_data = {
    joincode,
    create_only: true
};

test.beforeAll(async ({ browser }) => {
    apicontext = await createApiContext();
    p1 = (await getUserPage(browser, 'playerOne')) as PlayerGamePage;
});

test.beforeEach(async () => {
    const response = await apicontext.post('ops/run-game/', {
        headers: await p1.getAuthHeader(),
        data: { game_data: JSON.stringify(game_data) }
    });
    expect(response.status()).toBe(200);
});

test.afterAll(async () => {
    await p1.page.context().close();
    await apicontext.dispose();
});

test('round question cookies work properly', async () => {
    await p1.page.goto(gameUrl);
    await p1.expectCorrectQuestionHeading('1.1');

    await p1.roundSelector('3').click();
    await p1.expectCorrectQuestionHeading('3.1');

    await p1.goToQuestion('3.4');
    await p1.expectCorrectQuestionHeading('3.4');

    await p1.page.reload();
    await p1.expectCorrectQuestionHeading('3.4');
});

test('arrow keys change the active question', async () => {
    await p1.page.goto(gameUrl);
    await p1.goToQuestionFromKey('1.1');

    await p1.expectCorrectQuestionHeading('1.1');
    await p1.page.keyboard.press('ArrowRight');
    await asyncTimeout(200);
    await p1.expectCorrectQuestionHeading('1.2');
});

test('navigating away from the event page and back retains the active question', async () => {
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
