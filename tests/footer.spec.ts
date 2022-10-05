import { expect, test } from '@playwright/test';
import { createSelectorPromises, login } from './utils.js';
import type { Page } from '@playwright/test';

const footerLinks = ['Quiz', 'Leaderboard', 'Chat', 'Megaround', 'Scoring', 'Menu'];

test.describe('footer links display and navigate correctly', async () => {
    let page: Page;
    test.beforeAll(async ({ browser }) => {
        page = await browser.newPage();
        await login(page);
    });
    test.afterAll(async () => {
        await page.goto('/user/logout');
        await page.close();
    });

    test('home page does not have a nav bar', async () => {
        await page.goto('/');
        await expect(page.locator('nav')).not.toBeVisible();
    });

    test('team page only displays the menu link', async () => {
        await page.goto('/team');
        await expect(page).toHaveURL('/team');
        const visibleLinks = ['Menu'];
        const linkPromises = createSelectorPromises(page, visibleLinks, footerLinks);
        
        await Promise.all(linkPromises);
    });

    test('game join page only displays the menu link', async () => {
        await page.goto('/game/join');
        await expect(page).toHaveURL('/game/join');
        const visibleLinks = ['Menu'];
        const linkPromises = createSelectorPromises(page, visibleLinks, footerLinks);
        
        await Promise.all(linkPromises);
    });

    test('player game page displays all links except scoring', async () => {
        await page.goto('/game/1234');
        await expect(page).toHaveURL('/game/1234');
        const visibleLinks = footerLinks.filter((link) => link !== 'Scoring');    
        const linkPromises = createSelectorPromises(page, visibleLinks, footerLinks);
        
        await Promise.all(linkPromises);
    });
    
    test('Leaderboard link connects to the correct endpoint', async () => {
        await page.locator('p:has-text("Leaderboard")').click();
        await expect(page).toHaveURL('/game/1234/leaderboard');
    });

    test('Chat link connects to the correct endpoint', async () => {
        await page.locator('p:has-text("Chat")').click();
        await expect(page).toHaveURL('/game/1234/chat');
    });

    test('Megaround link connects to the correct endpoint', async () => {
        await page.locator('p:has-text("Megaround")').click();
        await expect(page).toHaveURL('/game/1234/megaround');
    });

    test('Quiz link connects to the correct endpoint', async () => {
        await page.locator('p:has-text("Quiz")').click();
        await expect(page).toHaveURL('/game/1234');
    });
    
    test('Menu opens when the icon is clicked', async () => {
        await page.locator('p:has-text("Menu")').click();
        await expect(page.locator('a:has-text("Logout")')).toBeVisible();
    });
});

// host/event-setup - menu only
// host/[joincode]/xxx all (scoring, not megaround)
