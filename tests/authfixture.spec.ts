import { expect, test as base } from '@playwright/test';

import type { APIRequestContext, Cookie, Page } from '@playwright/test';
import * as cookie from 'cookie';

const url = 'http://10.0.0.135:8000/user/login/';

export class AuthPage {
    readonly page: Page;
    readonly request: APIRequestContext;

    constructor(page: Page, request: APIRequestContext) {
        this.page = page;
        this.request = request;
    }

    async getCsrfToken() {
        const getResponse = await this.page.goto(url);
        const headers = (await getResponse?.allHeaders()) || {};
        const cookies = headers['set-cookie'];
        const csrfToken = (cookies && cookie.parse(cookies).csrftoken) || '';

        return csrfToken;
    }

    async setAuthCookie() {
        const csrfToken = await this.getCsrfToken();
        const requestContext = this.request;

        const resp = await requestContext.post(url, {
            headers: {
                Cookie: `csrftoken=${csrfToken}`,
                'X-CSRFToken': csrfToken,
                'content-type': 'application/json',
                accept: 'application/json'
            },
            data: {
                username: 'sample_admin',
                password: 'sample_admin'
            }
        });
        const headers = resp.headers();
        const cookies = headers['set-cookie'] || '';
        const jwt = <Cookie>(cookies ? cookie.parse(cookies).jwt : {});

        this.page.setExtraHTTPHeaders({ cookie: `jwt=${jwt}` });
    }
}

export const test = base.extend<{ authPage: AuthPage }>({
    authPage: async ({ page, request }, use) => {
        const authPage = new AuthPage(page, request);
        await authPage.setAuthCookie();

        await use(authPage);
    }
});

export { expect };