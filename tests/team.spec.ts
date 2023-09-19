import { expect, test } from './authConfigs.js';
import { createApiContext } from './utils.js';
import type { APIRequestContext } from '@playwright/test';

const TEST_TEAM_NAME = 'My Cool Team TEST';

let apicontext: APIRequestContext;

test.beforeAll(async () => {
    apicontext = await createApiContext();
});

test.afterEach(async ({ p1 }) => {
    const response = await apicontext.post('ops/delete/', {
        headers: await p1.getAuthHeader(),
        data: { type: 'team', team_names: [TEST_TEAM_NAME] }
    });
    expect(response.status()).toBe(200);
});

test.afterAll(async () => {
    await apicontext.dispose();
});

// test player lands on the correct page (should be /team and hellow world is the team)
// click to paly on a dff team, expeck drop down page
// click back then clikc creaate, expect create page

// test user w/ no teams goes to /create

test('correct handling of team creation', async ({ p1 }) => {
    await p1.page.goto('/team/create');
    // click create a new team
    // await p1.page.locator('button', { hasText: /create a new team/i }).click();
    // fill in team nam and submit
    // using .first() here as somehow we are resolving two elements, maybe it' picking up the label?
    const nameInput = p1.page.locator('input[name="team_name"]').first();

    // can't use a name longer than 100 characters
    await nameInput.fill('a'.repeat(101));
    await p1.page.locator('button#team-create-submit').click();
    await expect(p1.page.locator('p.error', { hasText: /too long/i }).first()).toBeVisible();

    await nameInput.fill(TEST_TEAM_NAME);
    await p1.page.locator('button#team-create-submit').click();
    // expect to be on game/join w/ a message about the team name (fow now anyway)
    await expect(p1.page).toHaveURL('/game/join');
    await expect(p1.page.locator('p', { hasText: /my cool team/i })).toBeVisible();
});

test('join team via code', async ({ p1 }) => {
    await p1.page.goto('/team/join');
    // await p1.page.locator('button', { hasText: 'Enter Team Password' }).click();
    await p1.page.locator('input[name="team_password"]').first().fill('supurb-glorify-bright');
    await p1.page.locator('button#team-password-submit').click();
    await expect(p1.page).toHaveURL('/game/join');
    await expect(p1.page.locator('p', { hasText: /hello world/i })).toBeVisible();
});

// TODO: we need a test for selecting an existing team
