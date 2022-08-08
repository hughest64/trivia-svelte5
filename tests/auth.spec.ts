import { expect, request, test } from '@playwright/test';

import * as cookie from 'cookie';

// TODO: env variable
const url = 'http://10.0.0.135:8000/user/login/';

// Import this into test files and run
export const getHostAuth = async (browser) => {
    // get a valid csrf token via the browser
    // const context = await browser.newContext();
    const page = await browser.newPage();
    const getResponse = await page.goto(url);
    const headers = (await getResponse?.allHeaders()) || {};
    const cookies = headers['set-cookie'];
    const csrfToken = (cookies && cookie.parse(cookies).csrftoken) || '';

    // use it to authenticate via the api and get back the jwt cookie
    const requestContext = await request.newContext({});
    await requestContext.post(url, {
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

    await requestContext.storageState({ path: 'staffUserAuth.json' });
    await page.close();
    await requestContext.dispose();
};

// example test structure
test.describe('authenticated requests', async () => {
    test.beforeAll(async ({ browser }) => await getHostAuth(browser));
    // test.use({ storageState: 'staffUserAuth.json' }); // TODO: will this work?

    test('we can make an authenticated rquest', async ({ browser }) => {
        // TODO: need a helper function for setting this jwt cookie
        const staffContext = await browser.newContext({ storageState: 'staffUserAuth.json' });
        const cookies = await staffContext.cookies();
        const jwt = cookies.find((cookie) => cookie.name === 'jwt') || {};
        
        const page = await staffContext.newPage();
        await page.setExtraHTTPHeaders({ cookie: `jwt=${jwt['value']}` });
        await page.goto('/');

        await expect(page).toHaveTitle(/Host Choice/);
        // expect(page.textContent('h1')).toBe('Greetings sample_admin');
    });
});
