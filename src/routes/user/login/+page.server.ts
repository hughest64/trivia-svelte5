import * as cookie from 'cookie';
import { fail, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST } from '$env/static/public';
import { getJwtPayload } from '$lib/utils';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch, locals }) => {
    if (locals.validtoken) throw redirect(302, '/team');
    const apiHost = PUBLIC_API_HOST;

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
            secure: false,
            sameSite: 'lax'
        });
    } catch (e) {
        console.error('could not connect to', apiHost);
        return { loaderror: 'Error: Could Not Connect to the Server' };
    }
};

const login: Action = async ({ cookies, fetch, request, url }) => {
    const formData = await request.formData();
    const username = formData.get('username');
    const password = formData.get('password');

    if (!username || !password) {
        return fail(403, { error: 'Please fill in both fields' });
    }
    const csrftoken = cookies.get('csrftoken') || '';

    const apiHost = PUBLIC_API_HOST;
    const response = await fetch(`${apiHost}/user/login/`, {
        method: 'POST',
        headers: {
            accept: 'application/json',
            'content-type': 'application/json',
            Cookie: `csrftoken=${csrftoken}`,
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ username, password })
    });

    const responseData = await response.json();

    if (!response.ok) {
        return fail(responseData.status, { error: responseData.detail });
    }

    const secureCookie = url.protocol === 'https:';
    const responseCookies = response.headers.get('set-cookie') || '';
    const jwt = cookie.parse(responseCookies)?.jwt;
    let guestUser = false;
    if (jwt) {
        const jwtData = getJwtPayload(jwt);
        guestUser = !!jwtData.guest_user;
        const expires = new Date((jwtData.exp as number) * 1000);
        cookies.set('jwt', jwt, { path: '/', expires, httpOnly: true, secure: secureCookie });
    }

    let next = url.searchParams.get('next');
    if (!next) {
        if (responseData?.user_data?.is_staff) {
            next = '/host/choice';
        } else {
            next = '/team';
        }
    }

    throw redirect(302, next);
};

export const actions = {
    default: login
};
