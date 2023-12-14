import { expect, test } from '@playwright/test';

test('a new test runs', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL('/');
});
