import * as cookie from 'cookie';
import { fail, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';
import type { Actions } from './$types';

// TODO:
// perhaps a load function should check for an existing jwt and redirect if it's valid, or remove it if it's not
// we should probably also have the api send a csrf cookie to handle the case of direct naigation
// (i.e, did't come from the log in page)

export const actions: Actions = {
    default: async ({ cookies, fetch, request, url }) => {
        const formData = await request.formData();
        const username = formData.get('username');
        const pass = formData.get('pass');
        const pass2 = formData.get('pass2');
        const email = formData.get('email');

        if (!username || !pass || !pass2 || !email) {
            return fail(400, { error: 'Please fill in all required fields' });
        }
        if (pass !== pass2) {
            return fail(400, { error: 'Passwords do not match!' });
        }

        const csrftoken = cookies.get('csrftoken') || '';

        const apiHost = env.PUBLIC_API_HOST;
        const response = await fetch(`${apiHost}/user/create`, {
            method: 'post',
            headers: {
                accept: 'application/json',
                'content-type': 'application/json',
                Cookie: `csrftoken=${csrftoken}`,
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ username, pass, pass2, email })
        });

        const respData = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: respData.detail });
        }

        const secureCookie = url.protocol === 'https:';
        const responseCookies = response.headers.get('set-cookie') || '';
        const jwt = cookie.parse(responseCookies)?.jwt;
        jwt && cookies.set('jwt', jwt, { path: '/', httpOnly: true, secure: Boolean(secureCookie) });

        // TODO: should we redirect or just send a nice message back to the page?
        const next = url.searchParams.get('next') || '';
        if (next) {
            return redirect(302, next as string);
        }
        throw redirect(302, '/team');
        // return { success: true };
    }
};
