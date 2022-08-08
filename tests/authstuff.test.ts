// BROKEN! this import will not be recognized may be some ts malakry
// could try that as a js file?
import * as auth from './authfixture.test';

auth.test('log in and go to root', async ({ authPage }) => {
    const page = authPage.page;
    await page.goto('/');

    // await auth.expect(page).toHaveTitle(/Host Choice/);
});