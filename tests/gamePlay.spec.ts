import { userAuthConfigs, expect, test } from './authConfigs.js';
import { defaultQuestionText } from './gamePages.js';
import { asyncTimeout, createApiContext } from './utils.js';
import type { APIRequestContext, APIResponse } from '@playwright/test';

// const revealDelay = 500;

const current = /current/;

const { playerOne, playerTwo, playerThree } = userAuthConfigs;

let apicontext: APIRequestContext;

const joincode_1 = '9904';
const joincode_2 = '9905';
const game1Url = `/game/${joincode_1}`;
const game2Url = `/game/${joincode_2}`;
const hostUrl = `/host/${joincode_1}`;

const game_1 = {
    joincode: joincode_1,
    rounds_to_play: 1,
    teams: 1,
    team_configs: {
        '1': {
            name: playerOne.teamName,
            players: [playerOne.username, playerTwo.username]
        }
    }
};

const game_2 = {
    joincode: joincode_2,
    rounds_to_play: 1,
    teams: 1,
    team_configs: {
        '1': {
            name: playerThree.teamName,
            players: [playerThree.username]
        }
    }
};

test.beforeAll(async () => {
    apicontext = await createApiContext();
});

test.afterAll(async () => {
    await apicontext.dispose();
});

test.beforeEach(async ({ host }) => {
    let response: APIResponse;
    response = await apicontext.post('/ops/run-game/', {
        headers: await host.getAuthHeader(),
        data: { game_data: JSON.stringify(game_1) }
    });
    expect(response.status()).toBe(200);

    response = await apicontext.post('/ops/run-game/', {
        headers: await host.getAuthHeader(),
        data: { game_data: JSON.stringify(game_2) }
    });
    expect(response.status()).toBe(200);
});

// TODO: this test should be completely reworked to check the new "current" logic and probably check the "go to current" link
test.skip('active round and question classes are applied properly', async ({ p1, host }) => {
    await p1.page.goto(game1Url);
    await host.page.goto(hostUrl);

    // check for current class on 1.1
    await expect(host.roundButton('1')).toHaveClass(current);
    await expect(p1.roundButton('1')).toHaveClass(current);
    await expect(p1.questionSelector('1.1')).toHaveClass(current);

    // host got to rd 2, reveal question2
    await host.roundButton('2').click();
    await host.revealQuestion('2.1');

    // 2.1 should be current
    // await asyncTimeout(revealDelay);
    await expect(host.roundButton('2')).toHaveClass(current);
    await expect(p1.roundButton('2')).toHaveClass(current);
    await expect(p1.questionSelector('2.1')).toHaveClass(current);

    // host go back to rd 1, reveal q5
    // 1.5 should not be set as current
    await host.roundButton('1').click();
    await host.revealQuestion('1.5');

    await expect(host.roundButton('1')).not.toHaveClass(current);

    // p1 should not be directed backwards? (not sure about this)
    await expect(p1.roundButton('2')).toHaveClass(current);
    await expect(p1.questionSelector('2.1')).toHaveClass(current);
});

test('question text reveals properly for players', async ({ p1, p2, p3, host }) => {
    await p1.page.goto(game1Url);
    await p2.page.goto(game1Url);
    await p3.page.goto(game2Url);
    await host.page.goto(hostUrl);

    // check 1.1 question text
    await expect(p1.questionTextField('1.1')).toHaveText(defaultQuestionText);
    await expect(p2.questionTextField('1.1')).toHaveText(defaultQuestionText);
    await expect(p3.questionTextField('1.1')).toHaveText(defaultQuestionText);

    // host reveals 1.1
    await host.expectQuestionToNotBeRevealed('1.1');
    await host.revealQuestion('1.1');
    await host.expectQuestionToBeRevealed('1.1');

    // popup should be displayed for p1 and host
    await expect(p1.dismissButton).toBeVisible();
    await expect(p2.dismissButton).toBeVisible();
    await expect(host.dismissButton).toBeVisible();
    await expect(p3.dismissButton).not.toBeVisible();

    // check question text
    // await asyncTimeout(revealDelay);
    await expect(p1.questionTextField('1.1')).not.toHaveText(defaultQuestionText);
    await expect(p2.questionTextField('1.1')).not.toHaveText(defaultQuestionText);
    await expect(p3.questionTextField('1.1')).toHaveText(defaultQuestionText);

    // test that the popup has closed
    await expect(p1.dismissButton).not.toBeVisible();
    await expect(host.dismissButton).not.toBeVisible();

    // test that no api error occured that would reset the reveal status
    await host.expectQuestionToBeRevealed('1.1');
});

test('auto reveal respects player settings', async ({ p1, p2, p3, host }) => {
    await p1.page.goto(game1Url);
    await p2.page.goto(game1Url);
    await p3.page.goto(game2Url);
    await host.page.goto(hostUrl);
    // host reveals 1.2
    await host.revealQuestion('1.2');
    // await asyncTimeout(1500);
    await host.expectQuestionToBeRevealed('1.2');
    await p1.expectCorrectQuestionHeading('1.2');
    await p2.expectCorrectQuestionHeading('1.1');
    await p3.expectCorrectQuestionHeading('1.1');
});

test('reveal all reveals all questions for a round', async ({ host }) => {
    await host.page.goto(hostUrl);
    // host reveals all for round 2
    await host.roundButton('2').click();
    await host.expectRoundToBe('2');

    // host find and click reveal all
    await host.revealQuestion('all');
    await asyncTimeout();

    const response = await apicontext.post('ops/validate/', {
        headers: await host.getAuthHeader(),
        data: { round_number: 2, joincode: joincode_1, type: 'validate_reveal_all' }
    });
    if (response.status() !== 200) {
        const details = await response.json();
        console.log(details);
        throw new Error('fail');
    }
});

test('round locks work properly', async ({ p1, p3, host }) => {
    await p1.page.goto(game1Url);
    await p3.page.goto(game2Url);
    await host.page.goto(hostUrl);

    await expect(p1.responseInput).toBeEditable();
    await expect(p3.responseInput).toBeEditable();

    const lockIconLabel = host.lockIconLabel('1');
    await host.expectLockedIconNotToBeVisible('1');
    await expect(lockIconLabel).toBeVisible();
    await lockIconLabel.click();

    await host.expectLockedIconToBeVisible('1');
    await expect(p1.responseInput).toBeDisabled();
    await expect(p3.responseInput).toBeEditable();
});

test('unlocking a round requires host confirmation', async ({ host }) => {
    await host.page.goto(hostUrl);
    // goto round 3
    await host.roundButton('3').click();
    await host.expectRoundToBe('3');

    // lock the round
    const lockIconLabel = host.lockIconLabel('3');
    await host.expectLockedIconNotToBeVisible('3');
    await lockIconLabel.click();
    await host.expectLockedIconToBeVisible('3');

    // try to unlock the round
    await lockIconLabel.click();
    await host.expectLockedIconToBeVisible('3');

    // confirm the unlock
    const btn = host.page.locator('.pop-content').locator('button');
    await btn.click();
    await expect(btn).not.toBeVisible();
    await host.expectLockedIconNotToBeVisible('3');
});
