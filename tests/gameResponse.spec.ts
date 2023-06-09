import { asyncTimeout, createApiContext } from './utils.js';
import { userAuthConfigs, test, expect } from './authConfigs.js';
import type { APIRequestContext, APIResponse } from '@playwright/test';

const submissionOne = 'answer for question';
const submissionTwo = 'a different answer';

const joincode_1 = '9902';
const joincode_2 = '9903';

const { playerOne, playerTwo, playerThree, playerFour } = userAuthConfigs;

let apicontext: APIRequestContext;

const game_1 = {
    joincode: joincode_1,
    teams: 2,
    team_configs: {
        '1': {
            name: playerOne.teamName,
            players: [playerOne.username, playerTwo.username]
        },
        '2': {
            name: playerThree.teamName,
            players: [playerThree.username]
        }
    }
};

const game_2 = {
    joincode: joincode_2,
    teams: 1,
    team_configs: {
        '1': {
            name: playerFour.teamName,
            players: [playerFour.username]
        }
    }
};

test.beforeAll(async () => {
    apicontext = await createApiContext();
});

test.afterAll(async () => {
    await apicontext.dispose();
});

test.beforeEach(async ({ p1 }) => {
    let response: APIResponse;
    response = await apicontext.post('/ops/run-game/', {
        headers: await p1.getAuthHeader(),
        data: { game_data: JSON.stringify(game_1) }
    });
    expect(response.status()).toBe(200);

    response = await apicontext.post('/ops/run-game/', {
        headers: await p1.getAuthHeader(),
        data: { game_data: JSON.stringify(game_2) }
    });
    expect(response.status()).toBe(200);
});

test('responses only update for the same team on the same event', async ({ p1, p2, p3, p4 }) => {
    await p1.page.goto(`/game/${joincode_1}`);
    await p2.page.goto(`/game/${joincode_1}`);
    await p3.page.goto(`/game/${joincode_1}`);
    await p4.page.goto(`/game/${joincode_2}`);

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

test('unsubmitted class is applied properly', async ({ p1 }) => {
    await p1.page.goto(`/game/${joincode_1}`);
    const responseInput = p1.page.locator('input[name="response_text"]');
    // expect the class not be to applied
    await expect(p1.page.locator('div#response-container')).not.toHaveClass(/notsubmitted/);

    await responseInput.fill('I know the answer');
    await expect(p1.page.locator('div#response-container')).toHaveClass(/notsubmitted/);

    await p1.page.locator('button:has-text("Submit")').click();
    await expect(p1.page.locator('div#response-container')).toHaveClass(/notsubmitted/);
});
