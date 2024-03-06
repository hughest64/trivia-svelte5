import { expect, test } from '@playwright/test';
import { asyncTimeout, getUserPage, triva_events, userAuthConfigs } from './config.js';

// 2 events
// 3 teams (all 3 teams on 1 event, 2 and p3 on a second event)
// 1 host

test('answer submissions are isolated per team', async ({ browser }) => {
    const eventData = triva_events.answer_submissions;
    const eventPage = `game/${eventData.joincode}`;
    // teammates
    const p1 = await getUserPage(browser, 'player_one');

    await p1.goto(eventPage);
    await expect(p1.locator('h4', { hasText: '1.1' })).toBeVisible();

    const p2 = await getUserPage(browser, 'player_two');
    await p2.goto(eventPage);
    await expect(p2.locator('h4', { hasText: '1.1' })).toBeVisible();

    // playing solo
    const p3 = await getUserPage(browser, 'player_three');
    await p3.goto(eventPage);
    await expect(p1.locator('h4', { hasText: '1.1' })).toBeVisible();

    const p1Input = p1.locator('input[name="response_text"]');
    await expect(p1Input).toBeEnabled();
    // p1 submits
    await p1Input.fill('the answer');
    await p1.locator('button', { hasText: /submit/i }).click({ timeout: 5000 });
    await asyncTimeout(500);
    // p2 sees it
    const p2Input = p2.locator('input[name="response_text"]');
    await expect(p2Input).toHaveValue('the answer');
    // p3 doesn't
    // p2 updates the resp
    // p1 sees it
    // p3 doesn't
});

test('question reveals and auto reveal work properly', async ({ browser }) => {
    const host = await getUserPage(browser, 'host_user');
    // auto reveal = true
    const p2 = await getUserPage(browser, 'player_two');
    // auto reveal = false
    const p3 = await getUserPage(browser, 'player_three');

    // host reveal question 1.1
    // host should see the btn active
    // players don't see any change (maybe no need to test?)
    // host reveal question 1.2
    // host should see the btn active
    // p2 should be on 1.2
    // p3 should see go to current
    // p3 click the btn
    // p3 should be on current
    // host click reveal all
    // reveal all btn is active (revealed?)
    // p2 is on 1.5
    // p3 sees go to 1.5

    // TODO: inlude this or separate test?
    // host locks rd1
    // p3 should not see go to current
    // if inlcude do we test answer inputs being disabled?
});

test('answer reveals work properly', async ({ browser }) => {
    const host = await getUserPage(browser, 'host_user');
    const p4 = await getUserPage(browser, 'player_four');

    // have preset responses and grades
    // have rd 1 pre-locked
    // p1 is on 1.1 and cannot see answer/pts/etc
    // host is on lb reveals answers
    // p1 can see items for rd1
    // p1 cannot see tiems for rd2, etc
});

test('host unlocking a round reqires confirmation', async ({ browser }) => {
    const host = await getUserPage(browser, 'host_user');
    // lock a round
    // see lock icon (class applied)
    // unlock
    // decline
    // can still see it
    // confirm
    // cannot see it
});
