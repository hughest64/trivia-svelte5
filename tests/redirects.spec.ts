import { expect, test } from './authConfigs.js';

const playerSelectedTeam = 'hello world';

test('non staff user accessing /host/choice redirects to team', async ({ p1 }) => {
    await p1.page.goto('/host/choice');
    await expect(p1.page).toHaveURL(/\/team/i);
});

test('non staff user accessing /host/event-setup redirects to team', async ({ p1 }) => {
    await p1.page.goto('/host/event-setup');
    await expect(p1.page).toHaveURL(/team/i);
});

test('non staff user accessing /host/1234 redirects to team', async ({ p1 }) => {
    await p1.page.goto('/host/1234');
    await expect(p1.page).toHaveURL(/team/i);
});

test('non staff user accessing /host/1234/controlboard redirects to team', async ({ p1 }) => {
    await p1.page.goto('/host/1234/controlboard');
    await expect(p1.page).toHaveURL(/team/i);
});

test('non staff user accessing /host/1234/score redirects to team', async ({ p1 }) => {
    await p1.page.goto('/host/1234/score');
    await expect(p1.page).toHaveURL(/team/i);
});

test('non staff user accessing /host/1234/leaderboard redirects to team', async ({ p1 }) => {
    await p1.page.goto('/host/1234/leaderboard');
    await expect(p1.page).toHaveURL(/team/i);
});

test('logged in user is redirected to /team when trying to go to /user/login', async ({ p1 }) => {
    await p1.page.goto('/user/login');
    await expect(p1.page).toHaveURL(/team/i);
});

test('logged in user is redirected to /team when trying to go to /', async ({ p1 }) => {
    await p1.page.goto('/');
    await expect(p1.page).toHaveURL(/team/i);
});

test('/team with a next query param redirects to next', async ({ p1 }) => {
    await p1.page.goto('/team?next=game/1234');
    await p1.page.selectOption('select#team-select', { label: playerSelectedTeam });
    await p1.page.locator('text=Choose This Team').click();

    await expect(p1.page).toHaveURL('/game/1234');
});

test('user with no active team is redirected to /team when trying to join a trivia event', async ({ host }) => {
    await host.page.goto('/game/1234');
    await expect(host.page).toHaveURL(/team/i);
});

test('user with no active team is redirected to /team when trying to access a leaderboard', async ({ host }) => {
    await host.page.goto('/game/1234/leaderboard');
    await expect(host.page).toHaveURL(/team/i);
});

test('user with no active team is redirected to /team when trying to access a megaround', async ({ host }) => {
    await host.page.goto('/game/1234/megaround');
    await expect(host.page).toHaveURL(/team/i);
});

test('user with no active team is redirected to /team when trying to access team chat', async ({ host }) => {
    await host.page.goto('/game/1234/chat');
    await expect(host.page).toHaveURL(/team/i);
});
