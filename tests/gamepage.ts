// see https://playwright.dev/docs/pom for information on this

import { expect } from '@playwright/test';
import { defaultTestConfig } from './utils.js';
import type { Locator, Page } from '@playwright/test';
import type { TestConfig } from './utils.js';

export class PlayerGamePage {
    readonly page: Page;
    readonly testConfig?: TestConfig;
    readonly responseInput: Locator;
    readonly submitButton: Locator;

    constructor(page: Page, testConfig: TestConfig = {}) {
        this.page = page;
        this.testConfig = { ...defaultTestConfig, ...testConfig };
        this.responseInput = page.locator('input[name="response_text"]');
        this.submitButton = page.locator('button', { hasText: 'Submit' });
        this.login();
    }

    questionHeading(text: string): Locator {
        return this.page.locator('h2', { hasText: text });
    }

    async expectInputValueToBe(text: string): Promise<void>{
        expect(await this.responseInput.inputValue()).toBe(text);
    }

    async expectInputValueToBeFalsy(): Promise<void> {
        expect(await this.responseInput.inputValue()).toBeFalsy();
    }

    async setResponse(text: string, submit = false): Promise<void> {
        await this.responseInput.fill(text);
        if (submit) await this.submitButton.click();
    }

    async login() {
        await this.page.goto(this.testConfig?.pageUrl as string);
        await this.page.locator('a', { hasText: 'Login' }).click();
        await this.page.locator('input[name="username"]').fill(this.testConfig?.username as string);
        await this.page.locator('input[name="password"]').fill(this.testConfig?.password as string);
        await this.page.locator('input[value="Submit"]').click();
    }

    async logout() {
        await this.page.goto('/user/logout');
    }

    // METHODS (all async)
    // url helper?
    // team select helper? (maybe not, players should have pre-set teams there) team testing is elsewhere
    // method for changing round numbers, question numbers
    // locator(s) for checking classes (current round, current question, active... notsubmtted, etc)
    // locator for question text (revealed vs. not)
    // locator for round locks
}
