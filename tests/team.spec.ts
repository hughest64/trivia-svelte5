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

// test player lands on the correct page (should be /team and hello world is the team)
// click to play on a dff team, expeck drop down page
// click back then clikc creaate, expect create page

test('team page routing', async ({ p1 }) => {
    await p1.page.goto('/');
    // p1 should have hello world as the default team
    const selectedTeam = p1.page.locator('h3', { hasText: /hello world/i });
    await expect(selectedTeam).toBeVisible();

    const goBtn = p1.page.locator('a', { hasText: /looks good/i });
    await expect(goBtn).toBeVisible();
    await goBtn.click();
    await expect(p1.page).toHaveURL(/\/game\/join/);
    await p1.page.goBack();
    await expect(selectedTeam).toBeVisible();

    // got to the team list
    const teamLink = p1.page.locator('a', { hasText: /existing team/i });
    await expect(teamLink).toBeVisible();
    await teamLink.click();
    await expect(p1.page).toHaveURL(/\/team\/list/i);

    // go to the password page (and back)
    const passwordLink = p1.page.locator('a', { hasText: /existing team/i });
    await expect(passwordLink).toBeVisible();
    await passwordLink.click();
    await expect(p1.page).toHaveURL(/\/team\/join/i);
    await p1.page.goBack();

    // go to create a new team
    const createLink = p1.page.locator('a', { hasText: /create a new team/i });
    await expect(createLink).toBeVisible();
    await createLink.click();
    await expect(p1.page).toHaveURL(/\/team\/create/i);
});

test('correct handling of team creation', async ({ p1 }) => {
    await p1.page.goto('/team/create');
    // fill in team name and submit
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
    await p1.page.locator('input[name="team_password"]').first().fill('supurb-glorify-bright');
    await p1.page.locator('button#team-password-submit').click();
    await expect(p1.page).toHaveURL('/game/join');
    await expect(p1.page.locator('p', { hasText: /hello world/i })).toBeVisible();
});

// TODO: we need a test for selecting an existing team
