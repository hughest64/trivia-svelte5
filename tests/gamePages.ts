// see https://playwright.dev/docs/pom for information on this

import { expect } from '@playwright/test';
import { defaultTestConfig } from './utils.js';
import type { Locator, Page } from '@playwright/test';
import type { TestConfig } from './utils.js';

export const defaultQuestionText = 'Please Wait for the Host to Reveal This Question';

class BasePage {
    readonly page: Page;
    readonly testConfig?: TestConfig;
    readonly dismissButton: Locator;

    constructor(page: Page, testConfig: TestConfig = {}) {
        this.page = page;
        this.testConfig = { ...defaultTestConfig, ...testConfig };
        this.dismissButton = page.locator('.pop').locator('button', { hasText: 'X' });
    }

    async login(joincode: string | null = null) {
        let destination = '/user/login?next=/game/join';
        if (joincode === null) {
            destination = `/user/login?next=${this.testConfig?.pageUrl as string}`;
        }

        await this.page.goto(destination);
        await this.page.locator('input[name="username"]').fill(this.testConfig?.username as string);
        await this.page.locator('input[name="password"]').fill(this.testConfig?.password as string);
        await this.page.locator('input[value="Submit"]').click();
        // join the game
        if (joincode !== null) {
            await this.page.locator('input[name="joincode"]').fill(joincode as string);
            await this.page.locator('button[type="submit"]').click();
        }
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
        // TODO: bring back auto-login, we'll need a testconfig arg for joincode in order to do so
        // this.login();
        // this.expectToLandOnGameUrl();
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

    async goToQuestion(text: string): Promise<void> {
        await this.questionSelector(text).click();
    }

    async expectQuestionTextNotToBeDefault(text: string): Promise<void> {
        // a value exists
        expect(this.questionTextField(text)).toBeTruthy();
        // but it's not the unrevealed value
        await expect(this.questionTextField(text)).not.toHaveText(defaultQuestionText);
    }

    async expectCorrectQuestionHeading(text: string): Promise<void> {
        await expect(this.questionHeading(text)).toHaveText(text);
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
    constructor(page: Page, testConfig: TestConfig) {
        super(page, testConfig);
        this.login();
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
