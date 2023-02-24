import { test as setup } from '@playwright/test';
import type { Page } from '@playwright/test';

interface AuthConfig {
    username: string;
    password: string;
}

export const authStorage: Record<string, string> = {
    playerFile: 'playwright/.auth/player.json',
    playerTwoFile: 'playwright/.auth/playertwo.json',
    playerThreeFile: 'playwright/.auth/playerthree.json',
    playerFourFile: 'playwright/.auth/playerfour.json',
    hostFile: 'playwright/.auth/host.json'
};

const login = async (page: Page, config: AuthConfig) => {
    await page.goto('/user/login');
    await page.locator('input[name="username"]').fill(config.username as string);
    await page.locator('input[name="password"]').fill(config.password as string);
    await page.locator('button', { hasText: 'Submit' }).click();
};

setup('authenticate player', async ({ page }) => {
    await login(page, { username: 'player', password: 'player' });
    await page.context().storageState({ path: authStorage.playerFile });
});

setup('authenticate player two', async ({ page }) => {
    await login(page, { username: 'player_two', password: 'player_two' });
    await page.context().storageState({ path: authStorage.playerTwoFile });
});

setup('authenticate player three', async ({ page }) => {
    await login(page, { username: 'player_three', password: 'player_three' });
    await page.context().storageState({ path: authStorage.playerThreeFile });
});

setup('authenticate player four', async ({ page }) => {
    await login(page, { username: 'player_four', password: 'player_four' });
    await page.context().storageState({ path: authStorage.playerFourFile });
});

setup('authenticate host', async ({ page }) => {
    await login(page, { username: 'sample_admin', password: 'sample_admin' });
    await page.context().storageState({ path: authStorage.hostFile });
});
