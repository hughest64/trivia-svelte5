import { expect, test } from './authConfigs.js';
import { createSelectorPromises } from './utils.js';

// TODO: don't use game 1234 and add an API call to make sure an event exists (use a 9900 series joincode)

const footerLinks = ['Quiz', 'Leaderboard', 'Chat', 'Controls', 'Megaround', 'Scoring', 'Menu'];

test('no nav on the login page', async ({ page }) => {
    await page.goto('/user/login');
    await expect(page.locator('nav')).not.toBeVisible();
});

test('no nav on the home (welcome) page', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('nav')).not.toBeVisible();
});

test('team page only displays the menu link', async ({ p1 }) => {
    await p1.page.goto('/team');
    await expect(p1.page).toHaveURL('/team');
    const visibleLinks = ['Menu'];
    const linkPromises = createSelectorPromises(p1.page, visibleLinks, footerLinks);

    await Promise.all(linkPromises);
});

test('game join page only displays the menu link', async ({ p1 }) => {
    await p1.page.goto('/game/join');
    await expect(p1.page).toHaveURL('/game/join');
    const visibleLinks = ['Menu'];
    const linkPromises = createSelectorPromises(p1.page, visibleLinks, footerLinks);

    await Promise.all(linkPromises);
});

test('player game page displays all links except scoring and controls', async ({ p1 }) => {
    await p1.page.goto('/game/1234');
    await expect(p1.page).toHaveURL('/game/1234');
    const visibleLinks = footerLinks.filter((link) => !['Scoring', 'Controls'].includes(link));
    const linkPromises = createSelectorPromises(p1.page, visibleLinks, footerLinks);

    await Promise.all(linkPromises);
});

test('Footer links navigate to the correct page', async ({ p1 }) => {
    await p1.page.goto('/game/1234');
    // leaderboard
    await p1.page.locator('p:has-text("Leaderboard")').click();
    await expect(p1.page).toHaveURL('/game/1234/leaderboard');
    // chat
    await p1.page.locator('p:has-text("Chat")').click();
    await expect(p1.page).toHaveURL('/game/1234/chat');
    // megaround
    await p1.page.locator('p:has-text("Megaround")').click();
    await expect(p1.page).toHaveURL('/game/1234/megaround');
    // back to the game
    await p1.page.locator('p:has-text("Quiz")').click();
    await expect(p1.page).toHaveURL('/game/1234');
    // menu
    await p1.page.locator('p:has-text("Menu")').click();
    await expect(p1.page.locator('a:has-text("Logout")')).toBeVisible();
});

test('only the menu is visible host the host choice page', async ({ host }) => {
    await host.page.goto('/host/choice');
    await expect(host.page).toHaveURL('/host/choice');
    const visibleLinks = ['Menu'];
    const linkPromises = createSelectorPromises(host.page, visibleLinks, footerLinks);

    await Promise.all(linkPromises);
});

test('only the menu is visible host the event setup', async ({ host }) => {
    await host.page.goto('/host/event-setup');
    await expect(host.page).toHaveURL('/host/event-setup');
    const visibleLinks = ['Menu'];
    const linkPromises = createSelectorPromises(host.page, visibleLinks, footerLinks);

    await Promise.all(linkPromises);
});

test('All links are visible on the host game page', async ({ host }) => {
    await host.page.goto('/host/1234');
    await expect(host.page).toHaveURL('/host/1234');
    const visibleLinks = footerLinks.filter((link) => !['Megaround', 'Chat'].includes(link));
    const linkPromises = createSelectorPromises(host.page, visibleLinks, footerLinks);

    await Promise.all(linkPromises);
});

test('Host links navigate to the correct page', async ({ host }) => {
    await host.page.goto('/host/1234');
    // leaderboard
    await host.page.locator('p:has-text("Leaderboard")').click();
    await expect(host.page).toHaveURL('/host/1234/leaderboard');
    // chat
    await host.page.locator('p:has-text("Controls")').click();
    await expect(host.page).toHaveURL('/host/1234/controlboard');
    // scoring
    await host.page.locator('p:has-text("Scoring")').click();
    await expect(host.page.locator('h1', { hasText: 'Scoring' })).toBeVisible();
    // back to the game
    await host.page.locator('p:has-text("Quiz")').click();
    await expect(host.page).toHaveURL('/host/1234');
    // open the menu
    await host.page.locator('p:has-text("Menu")').click();
    await expect(host.page.locator('a:has-text("Logout")')).toBeVisible();
});
