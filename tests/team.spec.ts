import { expect, test } from '@playwright/test';
import { createApiContext } from './utils.js';
import { getUserPage } from './authConfigs.js';
import type { PlayerGamePage } from './gamePages.js';
import type { APIRequestContext } from '@playwright/test';

const TEST_TEAM_NAME = 'My Cool Team TEST';

let p1: PlayerGamePage;
let apicontext: APIRequestContext;

test.beforeAll(async ({ browser }) => {
    apicontext = await createApiContext();
    p1 = (await getUserPage(browser, 'playerOne')) as PlayerGamePage;
});

test.afterEach(async () => {
    const response = await apicontext.post('ops/delete/', {
        headers: await p1.getAuthHeader(),
        data: { type: 'team', team_names: [TEST_TEAM_NAME] }
    });
    expect(response.status()).toBe(200);
});

test.afterAll(async () => {
    await p1.page.context().close();
    await apicontext.dispose();
});

test('correct handling of team creation', async () => {
    await p1.page.goto('/team');
    // click create a new team
    await p1.page.locator('button', { hasText: /create a new team/i }).click();
    // fill in team nam and submit
    // using .first() here as somehow we are resolving two elements, maybe it' picking up the label?
    await p1.page.locator('input[name="team_name"]').first().fill(TEST_TEAM_NAME);
    await p1.page.locator('button#team-create-submit').click();
    // expect to be on game/join w/ a message about the team name (fow now anyway)
    await expect(p1.page).toHaveURL('/game/join');
    await expect(p1.page.locator('p', { hasText: /my cool team/i })).toBeVisible();
});

test('join team via code', async () => {
    await p1.page.goto('/team');
    await p1.page.locator('button', { hasText: 'Enter Team Password' }).click();
    await p1.page.locator('input[name="team_password"]').first().fill('supurb-glorify-bright');
    await p1.page.locator('button#team-password-submit').click();
    await expect(p1.page).toHaveURL('/game/join');
    await expect(p1.page.locator('p', { hasText: /hello world/i })).toBeVisible();
});

// TODO: we need a test for selecting an exiting team (implement after the drop down is updated)
