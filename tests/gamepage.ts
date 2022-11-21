// see https://playwright.dev/docs/pom for information on this

// import { expect } from '@playwright/test';
import { defaultTestConfig, login as userLogin } from './utils.js';
import type { Locator, Page } from '@playwright/test';
import type { TestConfig } from './utils.js';

export class PlayerGamePage {
    readonly page: Page;
    readonly gamePage: string;
    readonly testConfig?: TestConfig;
    readonly responseInput: Locator;
    readonly submitButton: Locator;

    constructor(page: Page, gamePage: string, testConfig: TestConfig = {}) {
        this.page = page;
        this.gamePage = gamePage;
        this.testConfig = { ...defaultTestConfig, ...testConfig };
        this.responseInput = page.locator('input[name="response_text"]');
        this.submitButton = page.locator('button', { hasText: 'Submit' });
        this.login();
    }

    questionHeading(text: string): Locator {
        return this.page.locator('h2', { hasText: text });
    }

    async setResponse(text: string, submit = false): Promise<void> {
        await this.responseInput.fill(text);
        if (submit) await this.submitButton.click();
    }

    async login() {
        await userLogin(this.page, this.testConfig);
        await this.page.goto(this.gamePage);
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
