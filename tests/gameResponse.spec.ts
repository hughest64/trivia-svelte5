import { test } from '@playwright/test';
import { asyncTimeout } from './utils.js';
import { createApiContext } from './utils.js';
import { getUserPage, userAuthConfigs } from './authConfigs.js';
import { expect, type APIRequestContext, type APIResponse } from '@playwright/test';
import type { PlayerGamePage } from './gamePages.js';

const submissionOne = 'answer for question';
const submissionTwo = 'a different answer';

const joincode_1 = '9902';
const joincode_2 = '9903';

const { playerOne, playerTwo, playerThree, playerFour } = userAuthConfigs;

let apicontext: APIRequestContext;
let p1: PlayerGamePage;
let p2: PlayerGamePage;
let p3: PlayerGamePage;
let p4: PlayerGamePage;

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

test.beforeAll(async ({ browser }) => {
    apicontext = await createApiContext();
    p1 = (await getUserPage(browser, 'playerOne')) as PlayerGamePage;
    p2 = (await getUserPage(browser, 'playerTwo')) as PlayerGamePage;
    p3 = (await getUserPage(browser, 'playerThree')) as PlayerGamePage;
    p4 = (await getUserPage(browser, 'playerFour')) as PlayerGamePage;
});

test.afterAll(async () => {
    await p1.page.context().close();
    await p2.page.context().close();
    await p3.page.context().close();
    await p4.page.context().close();
    await apicontext.dispose();
});

test.beforeEach(async () => {
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

test('responses only update for the same team on the same event', async () => {
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
