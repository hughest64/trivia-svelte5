import * as cookie from 'cookie';
import { invalid, redirect } from '@sveltejs/kit';
import { getCookieObject, getFetchConfig } from '$lib/utils';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ request }) => {
    // go home user, you're already logged in
    const cookieObject = getCookieObject(request);
    if (cookieObject.jwt) {
        // TODO: goto /host/choice if staff which may require some user data in locals
        throw redirect(302, '/team');
    }
};

const login: Action = async ({ cookies, request }) => {
    const formData = await request.formData();
    const username = formData.get('username');
    const password = formData.get('password');

    if (!username || !password) {
        return invalid(403, { error: 'Please fill in both fields' });
    }

    // first, get a csrftoken
    const fetchConfig = getFetchConfig('GET');
    const getResponse = await fetch(`${apiHost}/user/login/`, fetchConfig);

    if (!getResponse.ok) {
        const getResponseData = await getResponse.json();
        return invalid(getResponseData.status, { error: getResponseData.detail });
    }

    const csrfCookie = cookie.parse(getResponse.headers.get('set-cookie') || '');
    const csrftoken = csrfCookie?.csrftoken || '';

    // TODO: use fetchConfig (maybe?)
    // then use the csrftoken to log in
    const postResponse = await fetch(`${apiHost}/user/login/`, {
        method: 'POST',
        headers: {
            accept: 'application/json',
            'content-type': 'application/json',
            Cookie: `csrftoken=${csrftoken}`,
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ username, password })
    });

    const postResponseData = await postResponse.json();

    if (!postResponse.ok) {
        return invalid(postResponseData.status, { error: postResponseData.detail });
    }

    // finally set both as cookies for later use
    const responseCookies = postResponse.headers.get('set-cookie') || '';
    const jwt = cookie.parse(responseCookies)?.jwt;

    responseCookies && cookies.set('jwt', jwt, { path: '/' });
    cookies.set('csrftoken', csrftoken, { expires: new Date(csrfCookie.expires), path: '/', sameSite: 'lax' });
    
    return { userdata: postResponseData.user_data };
};

export const actions = {
    default: login
};
