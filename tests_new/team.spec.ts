import { expect, test } from '@playwright/test';
import { getUserPage, userAuthConfigs } from './config.js';

const TEST_TEAM_NAME = 'My Cool Team';

test('create a team', async ({ browser }) => {
    const p1 = await getUserPage(browser, 'player_one');
    await p1.goto('/team');
    await p1.locator('a', { hasText: /create a new team/i }).click({ timeout: 5000 });
    // fill in team name and submit
    const nameInput = p1.locator('input[name="team_name"]');
    await expect(nameInput).toBeVisible();

    await nameInput.fill('1234');
    await p1.locator('button#team-create-submit').click();
    let errMsg = p1.locator('p.error', { hasText: /join code/i });
    await expect(errMsg).toBeVisible();

    // can't use a name longer than 100 characters
    await nameInput.fill('a'.repeat(101));
    await p1.locator('button#team-create-submit').click();
    errMsg = p1.locator('p.error', { hasText: /too long/i });
    await expect(errMsg).toBeVisible();

    await nameInput.fill(TEST_TEAM_NAME);
    await p1.locator('button#team-create-submit').click();
    // expect to be on game/join w/ a message about the team name (fow now anyway)
    await expect(p1.locator('h3', { hasText: /my cool team/i })).toBeVisible();

    await p1.locator('a', { hasText: /next/i }).click({ timeout: 5000 });

    await expect(p1).toHaveURL('/game/join');
});

test('a player can join a team with a password', async ({ browser }) => {
    const teamConfigs = userAuthConfigs.no_team_player.team_configs || [];
    const { name, password } = teamConfigs[0];

    const page = await getUserPage(browser, 'no_team_player');
    await page.goto('/team');
    await page.locator('a', { hasText: /join an existing team/i }).click({ timeout: 5000 });

    // expect the input to be empty
    await expect(page.locator('input[name="team_password"]')).toBeEmpty();
    await page.goto(`/team/join?password=${password}`);
    // expect the team name to be filled in and members populated
    await expect(page.locator('input[name="team_password"]')).toHaveValue(password);
    await expect(page.locator('h2', { hasText: `Team: ${name}` })).toBeVisible();

    await page.locator('button', { hasText: /join team/i }).click({ timeout: 5000 });
    await expect(page).toHaveURL('/game/join');
    // expect the team name to be visible
    await expect(page.locator('h2', { hasText: name })).toBeVisible();
});

test('a player can select a new active team', async ({ browser }) => {
    const userData = userAuthConfigs.two_team_player;
    const teamNames = userData.team_names || [];

    const page = await getUserPage(browser, 'two_team_player');
    await page.goto('/team');

    // we should have 2 teams to choose from in the same order as our team name array
    const selectOptions = page.locator('option');
    await expect(selectOptions).toHaveCount(2);
    await expect(selectOptions.first()).toHaveText(teamNames[0]);

    // select a new team
    await page.locator('select').selectOption({ label: teamNames[1] });
    await page.locator('button', { hasText: /let's play/i }).click({ timeout: 5000 });
    await expect(page).toHaveURL('/game/join');

    // expect the new selected team name to be visible
    await expect(page.locator('h2', { hasText: teamNames[1] })).toBeVisible();
});
