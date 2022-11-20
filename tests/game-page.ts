// see https://playwright.dev/docs/pom for information on this

// import { expect } from '@playwright/test';
import { defaultTestConfig } from './utils';
import type { /* Locator,*/ Page } from '@playwright/test';
import type { TestConfig } from './utils';

export class PlayerGamePage {
    readonly page: Page;
    testConfig?: TestConfig;

    constructor (page: Page, testConfig: TestConfig = {}) {
        this.page = page;
        // merge user config into the default config
        this.testConfig =  { ...defaultTestConfig,  ...testConfig };
        // default submission values?
    }

    // METHODS (all async)
    // login (can assign the helper here?), login then gotoGamePage
    // gotoGamePage(joincode)
    // lougout (just goto('/user/logout'))
    // checkQuestionHeader (expcept h2 to be 1.1, etc)
    // locator for response input
    // url helper?
    // team select helper? (maybe not, players should have pre-set teams there) team testing is elsewhere
    // mehtod for changing round numbers, question numbers
    // locator(s) for checking classes (current round, current question, active... notsubmtted, etc)
    // method for for submmitting
    // locator for question text (revevealed vs. not)
    // locator for round locks
}