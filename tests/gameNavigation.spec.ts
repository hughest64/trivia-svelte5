import { expect, test } from '@playwright/test';
import { asyncTimeout, loginToGame, resetEventData } from './utils.js';

/**
 * TODO:
 * - test swiping (how to do this?)
 */

const submission = 'a different answer';

test.beforeEach(async ({ page }) => {
    await loginToGame(page, { joincode: '1234' });
});

test.afterEach(async ({ page }) => {
    await page.goto('/user/logout');
});

test.afterEach(async () => {
    await resetEventData();
});

test('round question cookies work properly', async ({ page }) => {
    expect(await page.textContent('h4')).toBe('1.1');

    await page.locator('.round-selector').locator('button:has-text("3")').click();
    await asyncTimeout(200);
    expect(await page.textContent('h4')).toBe('3.1');

    const questionThree = page.locator('.question-selector').locator('button:has-text("4")');
    await questionThree.click();
    await asyncTimeout(200);
    expect(await page.textContent('h4')).toBe('3.4');

    await page.reload();
    expect(await page.textContent('h4')).toBe('3.4');
});

test('arrow keys change the active question', async ({ page }) => {
    expect(await page.textContent('h4')).toBe('1.1');
    await page.keyboard.press('ArrowRight');
    await asyncTimeout(150);
    expect(await page.textContent('h4')).toBe('1.2');
});

test('unsubmitted class is applied properly', async ({ page }) => {
    const responseInput = page.locator('input[name="response_text"]');
    // expect the class not be to applied
    await expect(page.locator('div.notsubmitted')).not.toBeVisible();
    await responseInput.fill(submission);
    await expect(page.locator('div.notsubmitted')).toBeVisible();

    await page.locator('button:has-text("Submit")').click();
    await expect(page.locator('div.notsubmitted')).not.toBeVisible();
});

test('navigating away from the event page and back retains the active question', async ({ page }) => {
    expect(await page.textContent('h4')).toBe('1.1');
    await page.locator('.question-selector').locator('id=1.3').click();
    await asyncTimeout(500);
    await expect(page.locator('.question-row').locator('h4', { hasText: '1.3' })).toBeVisible();

    // navigate to another page
    await page.locator('p', { hasText: 'Chat' }).click();
    await page.locator('p', { hasText: 'Quiz' }).click();
    await expect(page.locator('h2', { hasText: 'General Knowledge' })).toBeVisible();
    await asyncTimeout(500);

    // try to move again
    await page.locator('.question-selector').locator('id=1.4').click();
    await asyncTimeout(500);
    expect(await page.textContent('h4')).toBe('1.4');
});
