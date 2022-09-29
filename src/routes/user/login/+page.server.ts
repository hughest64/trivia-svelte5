import * as cookie from 'cookie';
import { invalid, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
    // go home user, you're already logged in
    // TODO: this is flaky a f and does not cut it
    // if (cookies.get('jwt')) {
    //     // TODO: goto /host/choice if staff
    //     // I think the solution here might be to add is_staff to the jwt payload
    //     // and use a decode lib to get the data?
    //     throw redirect(302, '/team');
    // }

    // get a csrf token from the api
    const getResponse = await fetch(`${apiHost}/user/login/`);
    if (!getResponse.ok) {
        const getResponseData = await getResponse.json();
        return invalid(getResponseData.status, { error: getResponseData.detail });
    }

    const csrfCookie = cookie.parse(getResponse.headers.get('set-cookie') || '');
    const csrftoken = csrfCookie?.csrftoken || '';

    cookies.set('csrftoken', csrftoken, { expires: new Date(csrfCookie.expires), path: '/', sameSite: 'lax' });
};

const login: Action = async ({ cookies, request, url }) => {
    const formData = await request.formData();
    const username = formData.get('username');
    const password = formData.get('password');

    if (!username || !password) {
        return invalid(403, { error: 'Please fill in both fields' });
    }
    const csrftoken = cookies.get('csrftoken') || '';

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
        return invalid(responseData.status, { error: responseData.detail });
    }
    
    const responseCookies = response.headers.get('set-cookie') || '';
    const jwt = cookie.parse(responseCookies)?.jwt;
    jwt && cookies.set('jwt', jwt, { path: '/' });

    // TODO: we need an algorithm to determine redirects
    // - prefer query param, but check for authorization
    // - if host goto /host/choice - maybe this should just be /host?
    // - else goto /team
    const next = url.searchParams.get('next') || '/team';
    throw redirect(302, next);
};


export const actions = {
    login,
    // github, // (and google?),
    // google,
    // create // (new account)
};
