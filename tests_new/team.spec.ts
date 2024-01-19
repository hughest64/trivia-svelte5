import { expect, test } from '@playwright/test';
import { getUserPage } from './config.js';

const TEST_TEAM_NAME = 'My Cool Team';

test('create a team', async ({ browser }) => {
    const p1 = await getUserPage(browser, 'player_one');
    await p1.goto('/team/create');
    // fill in team name and submit
    // using .first() here as somehow we are resolving two elements, maybe it' picking up the label?
    const nameInput = p1.locator('input[name="team_name"]').first();

    // can't use a name longer than 100 characters
    await nameInput.fill('a'.repeat(101));
    await p1.locator('button#team-create-submit').click();
    const errMsg = p1.locator('p.error', { hasText: /too long/i }).first();
    await expect(errMsg).toBeVisible();

    await nameInput.fill(TEST_TEAM_NAME);
    await p1.locator('button#team-create-submit').click();
    // expect to be on game/join w/ a message about the team name (fow now anyway)
    await expect(p1).toHaveURL('/game/join');
    await expect(p1.locator('p', { hasText: /my cool team/i })).toBeVisible();
});
