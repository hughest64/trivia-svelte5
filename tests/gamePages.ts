// see https://playwright.dev/docs/pom for information on this

import { expect } from '@playwright/test';
import { defaultTestConfig } from './utils.js';
import type { Browser, Cookie, Locator, Page } from '@playwright/test';
import type { TestConfig } from './utils.js';
// this could be loaded in the test file and passed into the config

export const defaultQuestionText = 'Please Wait for the Host to Reveal This Question';

// this works, but a whole player config would be nice
type StorageKey = 'playerFile' | 'playerTwoFile' | 'playerThreeFile' | 'playerFourFile' | 'hostFile';
export const authStorage: Record<StorageKey, string> = {
    playerFile: 'playwright/.auth/player.json',
    playerTwoFile: 'playwright/.auth/playertwo.json',
    playerThreeFile: 'playwright/.auth/playerthree.json',
    playerFourFile: 'playwright/.auth/playerfour.json',
    hostFile: 'playwright/.auth/host.json'
};

export interface GetFromContextTypes {
    userCookies: Cookie[];
    page: Page;
}
export const getPageFromContext = async (
    browser: Browser,
    storagePath: string | StorageKey
): Promise<GetFromContextTypes> => {
    const filePath = authStorage[storagePath as StorageKey] || storagePath;
    const context = await browser.newContext({ storageState: filePath });
    const userCookies = await context.cookies();
    const page = await context.newPage();

    return { userCookies, page };
};

class BasePage {
    readonly page: Page;
    readonly testConfig?: TestConfig;
    readonly dismissButton: Locator;

    constructor(page: Page, testConfig: TestConfig = {}) {
        this.page = page;
        this.testConfig = { ...defaultTestConfig, ...testConfig };
        this.dismissButton = page.locator('.pop').locator('button', { hasText: 'X' });
    }

    async useAuthConfig() {
        if (!this.testConfig?.authStoragePath) {
            throw new Error('a file path for authStoragePath is required for method useAuthConfig');
        }
        const cookies = this.testConfig?.cookies || [];
        // TODO: use this once we actually properly set an expiration on the cookie
        // const expiration = (cookies && cookies.find((cookie) => cookie.name === 'jwt')?.expires) || 0;
        // if (!cookies || (expiration as number) < 1234) {
        if (cookies.length === 0) {
            await this.login();
            await this.page.context().storageState({ path: this.testConfig?.authStoragePath });
        }
    }

    // NOTE: not needed to use this with the custom fixtures as they auto-login
    async login(username?: string, password?: string) {
        const uname = username || this.testConfig?.username || '';
        const pword = password || this.testConfig?.password || '';
        await this.page.goto('/user/login');
        await this.page.locator('input[name="username"]').fill(uname);
        await this.page.locator('input[name="password"]').fill(pword);
        await this.page.locator('button', { hasText: 'Submit' }).click();
        // TODO: add an expect so that we know when we fail on log in immediately
    }

    async logout() {
        await this.page.goto('/user/logout');
    }

    async expectToLandOnGameUrl() {
        await expect(this.page).toHaveURL(this.testConfig?.pageUrl as string);
    }

    roundButton(text: string): Locator {
        return this.page.locator('.round-selector').locator('button', { hasText: text });
    }
}

export class PlayerGamePage extends BasePage {
    readonly responseInput: Locator;
    readonly submitButton: Locator;

    constructor(page: Page, testConfig: TestConfig = {}) {
        super(page, testConfig);
        this.responseInput = page.locator('input[name="response_text"]');
        this.submitButton = page.locator('button', { hasText: 'Submit' });
    }

    questionHeading(text: string): Locator {
        return this.page.locator('h4', { hasText: text });
    }

    questionTextField(text: string): Locator {
        return this.page.locator(`id=${text}-text`);
    }

    questionSelector(text: string): Locator {
        return this.page.locator('.question-selector').locator(`id=${text}`);
    }

    async joinGame(joincode: string): Promise<void> {
        await this.page.goto('/game/join');
        await this.page.locator('input[name="joincode"]').fill(joincode);
        await this.page.locator('button[type="submit"]').click();
    }

    async goToQuestion(text: string): Promise<void> {
        await this.questionSelector(text).click();
    }

    async expectQuestionTextNotToBeDefault(text: string): Promise<void> {
        // a value exists
        expect(this.questionTextField(text)).toBeTruthy();
        // but it's not the unrevealed value
        await expect(this.questionTextField(text)).not.toHaveText(defaultQuestionText);
    }

    // NOTE: .first() is generally frowned on here as we shouldn't allow a seletor to resolve
    // mutliple elements. However, we have a unique situation in how the question component is updated
    // during the transition it appears there that there are two cards with the same class
    async expectCorrectQuestionHeading(text: string): Promise<void> {
        await expect(this.page.locator('.question-key').first()).toHaveText(text);
    }

    async expectInputValueToBe(text: string): Promise<void> {
        expect(await this.responseInput.inputValue()).toBe(text);
    }

    async expectInputValueToBeFalsy(): Promise<void> {
        expect(await this.responseInput.inputValue()).toBeFalsy();
    }

    async setResponse(text: string, opts = { submit: false }): Promise<void> {
        await this.responseInput.fill(text);
        if (opts.submit) await this.submitButton.click();
    }

    async submitResponse(): Promise<void> {
        await this.submitButton.click();
    }
}

export class HostGamePage extends BasePage {
    constructor(page: Page, testConfig: TestConfig = {}) {
        super(page, testConfig);
    }
    questionSlider(text: string): Locator {
        return this.page.locator(`label[for="${text}"]`);
    }

    revealedClass(text: string): Locator {
        return this.questionSlider(text).locator('.revealed');
    }

    lockIconLabel(text: string): Locator {
        return this.page.locator(`id=rd-${text}`);
    }

    lockIcon(text: string): Locator {
        return this.lockIconLabel(text).locator('span.checked');
    }

    async expectLockedIconToBeVisible(text: string): Promise<void> {
        await expect(this.lockIcon(text)).toBeVisible();
    }

    async expectLockedIconNotToBeVisible(text: string): Promise<void> {
        await expect(this.lockIcon(text)).not.toBeVisible();
    }

    async revealQuestion(text: string): Promise<void> {
        await this.questionSlider(text).click();
    }

    async expectQuestionToBeRevealed(text: string): Promise<void> {
        await expect(this.revealedClass(text)).toBeVisible();
    }

    async expectQuestionToNotBeRevealed(text: string): Promise<void> {
        await expect(this.revealedClass(text)).not.toBeVisible();
    }

    async expectRoundToBe(text: string) {
        await expect(this.roundButton(text)).toHaveText(text);
    }
}
