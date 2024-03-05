import { expect, test } from '@playwright/test';
import { asyncTimeout, getUserPage, triva_events, userAuthConfigs } from './config.js';

test('a bad joincode', async ({ browser }) => {
    const joincode = '99999';
    const page = await getUserPage(browser, 'player_two');
    await page.goto('/game/join');
    await page.locator('input[name="joincode"]').fill(joincode);
    await page.locator('button', { hasText: /join game/i }).click({ timeout: 5000 });

    await expect(page.locator('p.error')).toHaveText(`Event with join code ${joincode} does not exist`);
});

test('only one team member can join a single device game', async ({ browser }) => {
    const joincode = triva_events.player_limit_test.joincode;

    const p3 = await getUserPage(browser, 'player_three');
    const p4 = await getUserPage(browser, 'player_four');

    // p3 joins the event first
    await p3.goto('/game/join');
    await p3.locator('input[name="joincode"]').fill(joincode, { timeout: 5000 });
    await p3.locator('button', { hasText: /join game/i }).click({ timeout: 5000 });
    await expect(p3.locator('h2', { hasText: /you're playing at/i })).toBeVisible();
    await p3.locator('button', { hasText: /looks good/i }).click({ timeout: 5000 });
    await expect(p3).toHaveURL(`/game/${joincode}`);

    // p4 cannot join the same event
    await p4.goto('/game/join');
    await p4.locator('input[name="joincode"]').fill(joincode, { timeout: 5000 });
    await p4.locator('button', { hasText: /join game/i }).click({ timeout: 5000 });

    await expect(p4.locator('p', { hasText: /sorry/i })).toBeVisible();
    let teamLink = p4.locator('a', { hasText: /go here to create a new team/i });
    await expect(teamLink).toBeVisible();
    await teamLink.click({ timeout: 5000 });
    await expect(p4).toHaveURL('/team/create');

    // p4 also cannot navigate directly to the game
    await p4.goto(`/game/${joincode}`);
    teamLink = p4.locator('a', { hasText: /create a new team/i });
    await expect(teamLink).toBeVisible();
    await teamLink.click({ timeout: 5000 });
    await expect(p4).toHaveURL('/team/create');
});

test('a player is requried to verify the event before joining', async ({ browser }) => {
    const userTeams = userAuthConfigs.player_three.team_names || [];
    const joincode = triva_events.player_limit_test.joincode;

    const page = await getUserPage(browser, 'player_three');

    await page.goto('/game/join');
    await page.locator('input[name="joincode"]').fill(joincode, { timeout: 5000 });
    await page.locator('button', { hasText: /join game/i }).click({ timeout: 5000 });
    await expect(page.locator('h2', { hasText: /you're playing at/i })).toBeVisible();

    // maybe that wasn't the right code?
    await page.locator('button', { hasText: /that's not right/i }).click({ timeout: 5000 });
    // NOTE adding the delay and use of .last() here as Svelte transitions cause
    // two game code inputs to be visible while the transistion is running;
    await asyncTimeout(200);
    await expect(page.locator('input[name="joincode"]').last()).toBeEmpty();
    // it was right after all
    await page.locator('input[name="joincode"]').last().fill(joincode, { timeout: 5000 });
    await page.locator('button', { hasText: /join game/i }).click({ timeout: 5000 });
    await page.locator('button', { hasText: /looks good/i }).click({ timeout: 5000 });
    await expect(page).toHaveURL(`/game/${joincode}`);

    // check that a leaderboard entry was created and loaded
    await page.locator('a', { hasText: /leaderboard/i }).click({ timeout: 5000 });
    const lbe = page.locator('a').locator('div.team-name').locator('h3.team-name-display', { hasText: userTeams[0] });
    await expect(lbe).toBeVisible();
});
