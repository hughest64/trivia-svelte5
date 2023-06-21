import { env } from '$env/dynamic/public';
import { fail, redirect } from '@sveltejs/kit';
import * as cookie from 'cookie';
import { getJwtPayload } from '$lib/utils';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch, params, url }) => {
    // no need to fetch a token if we have one.
    if (cookies.get('jwt')) return;

    const csrftoken = cookies.get('csrftoken') || '';
    console.log(csrftoken);

    // request a long-lived token for auto-login
    const resp = await fetch(`${env.PUBLIC_API_HOST}/user/refresh`, {
        method: 'POST',
        headers: {
            accept: 'application/json',
            'content-type': 'application/json',
            Cookie: `csrftoken=${csrftoken}`,
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ token: params.token })
    });

    if (!resp.ok) {
        const respData = await resp.json();
        return fail(resp.status, { error: respData.detail });
    }

    // set the long-lived token as a cookie
    const secureCookie = url.protocol === 'https:';
    const responseCookies = resp.headers.get('set-cookie') || '';
    const jwt = cookie.parse(responseCookies)?.jwt;
    if (jwt) {
        const jwtData = getJwtPayload(jwt);
        const expires = new Date((jwtData.exp as number) * 1000);
        cookies.set('jwt', jwt, { path: '/', expires, httpOnly: true, secure: secureCookie });
    }
};

export const actions: Actions = {
    default: async ({ request, fetch, params }) => {
        const data = await request.formData();
        const { pass1, pass2 } = Object.fromEntries(data);

        if (pass1 !== pass2) {
            return fail(400, { error: 'Passwords do not match' });
        }

        const token = params.token;

        const resp = await fetch(`${env.PUBLIC_API_HOST}/user/reset`, {
            method: 'post',
            headers: { accept: 'application/json', 'content-type': 'application/json' },
            body: JSON.stringify({ pass1, pass2, token })
        });

        if (!resp.ok) {
            const respData = await resp.json();
            return fail(resp.status, { error: respData.detail });
        }

        throw redirect(301, '/team');
    }
};
