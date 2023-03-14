import * as cookie from 'cookie';
import { fail, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch, locals, url }) => {
    const apiHost = env.PUBLIC_API_HOST;
    const secureCookie = url.protocol === 'https:';

    if (locals.validtoken) throw redirect(302, '/team');

    try {
        // get a csrf token from the api
        const getResponse = await fetch(`${apiHost}/user/login/`);
        if (!getResponse.ok) {
            const getResponseData = await getResponse.json();
            return fail(getResponseData.status, { error: getResponseData.detail });
        }

        const csrfCookie = cookie.parse(getResponse.headers.get('set-cookie') || '');
        const csrftoken = csrfCookie?.csrftoken || '';

        cookies.set('csrftoken', csrftoken, {
            expires: new Date(csrfCookie.expires),
            path: '/',
            secure: Boolean(secureCookie),
            sameSite: 'lax'
        });
    } catch (e) {
        console.error('cound not connect to', apiHost);
        return { loaderror: 'Error: Could Not Connect to the Server' };
    }
};

// guest login
const guestLogin: Action = async ({ cookies, fetch, url }) => {
    const apiHost = env.PUBLIC_API_HOST;
    const secureCookie = url.protocol === 'https:';
    const csrftoken = cookies.get('csrftoken') || '';
    const response = await fetch(`${apiHost}/user/guest/`, {
        method: 'POST',
        headers: {
            accept: 'application/json',
            'content-type': 'application/json',
            Cookie: `csrftoken=${csrftoken}`,
            'X-CSRFToken': csrftoken
        }
    });

    const responseData = await response.json();

    if (!response.ok) {
        return fail(responseData.status, { error: responseData.detail });
    }

    const responseCookies = response.headers.get('set-cookie') || '';
    const jwt = cookie.parse(responseCookies)?.jwt;
    jwt && cookies.set('jwt', jwt, { path: '/', secure: Boolean(secureCookie), httpOnly: true });
    const next = url.searchParams.get('next') || '/team';

    throw redirect(302, next);
};

export const actions = {
    default: guestLogin
};
