import * as cookie from 'cookie';
import { redirect } from '@sveltejs/kit';
import { getCookieObject, getFetchConfig } from '$lib/utils';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ request }) => {
    // go home user, you're already logged in
    const cookieObject = getCookieObject(request);
    if (cookieObject.jwt) {
        throw redirect(302, '/');
    }
};

export const POST: Action = async ({ request, setHeaders, url }) => {
    const formData = await request.formData();
    const username = formData.get('username');
    const password = formData.get('password');

    if (!username || !password) {
        return { errors: { message: 'Please fill in both fields' } };
    }

    // first, get a csrftoken
    const fetchConfig = getFetchConfig('GET');
    const getResponse = await fetch(`${apiHost}/user/login/`, fetchConfig);

    if (!getResponse.ok) {
        const getResponseData = await getResponse.json();
        return { errors: { message: getResponseData.detail } };
    }

    const csrfCookie = getResponse.headers.get('set-cookie') || '';
    const csrftoken = (csrfCookie && cookie.parse(csrfCookie)?.csrftoken) || '';

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
        return { errors: { message: postResponseData.detail } };
    }

    // TODO: return data to the login page then redirect from there once
    // https://github.com/sveltejs/kit/issues/6015 is resolved
    // const responseData: UserData = await postResponse.json();

    // finally set both as cookies for later use
    const responseCookies = postResponse.headers.get('set-cookie');
    responseCookies && setHeaders({ 'set-cookie': [responseCookies, csrfCookie] });
    const next = url.searchParams.get('next') || '/';

    return { location: next };
};
