import { env } from '$env/dynamic/public';
import { error, fail, redirect } from '@sveltejs/kit';
import * as cookie from 'cookie';
import { getJwtPayload } from '$lib/utils';
import type { Actions, PageServerLoad } from './$types';

/**
 * TODO: right now there is no path for a logged in user to change their password
 * We need a path for that, perhaps:
 * - the token should be optional (still needs to be valid if present)
 * - if there is no token, a valid jwt cookie is required
 * - if neither condition is met, redirect to /forgot?
 */

export const load: PageServerLoad = async ({ cookies, fetch, params, url }) => {
    // no need to fetch a token if we have one.
    if (cookies.get('jwt')) return;

    const csrftoken = cookies.get('csrftoken') || '';

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
        if (respData?.reason === 'authentication_failed') {
            throw redirect(307, '/user/forgot');
        }
        const message = respData?.detail || 'an error ocurred';
        throw error(resp.status, { message });
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
    default: async ({ cookies, request, fetch, params }) => {
        const data = await request.formData();
        const { pass1, pass2 } = Object.fromEntries(data);

        if (pass1 !== pass2) {
            return fail(400, { error: 'Passwords do not match' });
        }

        // get the token from the url param or the cookie of an already logged in user
        const token = params.token || cookies.get('jwt') || '';

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