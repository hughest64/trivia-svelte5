import { expect, test } from './fixtures.js';
import { resetEventData } from './utils.js';

test.afterAll(async () => {
    await resetEventData();
});

test('correct handling of team creation', async ({ p1Page }) => {
    await p1Page.page.goto('/team');
    // click create a new team
    await p1Page.page.locator('button', { hasText: /create a new team/i }).click();
    // fill in team nam and submit
    // using .first() here as somehow we are resolving two elements, maybe it' picking up the label?
    await p1Page.page.locator('input[name="team_name"]').first().fill('My Cool Team TEST');
    await p1Page.page.locator('button#team-create-submit').click();
    // expect to be on game/join w/ a message about the team name (fow now anyway)
    await expect(p1Page.page).toHaveURL('/game/join');
    await expect(p1Page.page.locator('p', { hasText: /my cool team/i })).toBeVisible();
});

test('join team via code', async ({ p1Page }) => {
    await p1Page.page.goto('/team');
    await p1Page.page.locator('button', { hasText: 'Enter Team Password' }).click();
    await p1Page.page.locator('input[name="team_password"]').first().fill('supurb-glorify-bright');
    await p1Page.page.locator('button#team-password-submit').click();
    await expect(p1Page.page).toHaveURL('/game/join');
    await expect(p1Page.page.locator('p', { hasText: /hello world/i })).toBeVisible();
});

// TODO: we need a test for selecting an exiting team
