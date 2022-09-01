import * as cookie from 'cookie';
import { redirect } from '@sveltejs/kit';
import { getCookieObject, getFetchConfig } from '$lib/utils';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ request }) => {
    // go home user, you're already logged in
    const cookieObject = getCookieObject(request);
    // TODO: goto /host/choice if the user is staff (so jwt by itself is not good enough)
    if (cookieObject.jwt) {
        throw redirect(302, '/team');
    }
};

export const POST: Action = async ({ setHeaders, url }) => {
    // first, get a csrftoken
    const fetchConfig = getFetchConfig('GET');
    const getResponse = await fetch(`${apiHost}/user/guest/`, fetchConfig);

    if (!getResponse.ok) {
        const getResponseData = await getResponse.json();
        return { errors: { message: getResponseData.detail } };
    }

    const csrfCookie = getResponse.headers.get('set-cookie') || '';
    const csrftoken = (csrfCookie && cookie.parse(csrfCookie)?.csrftoken) || '';

    // TODO: use fetchConfig (maybe?)
    // then use the csrftoken to log in
    const postResponse = await fetch(`${apiHost}/user/guest/`, {
        method: 'POST',
        headers: {
            accept: 'application/json',
            'content-type': 'application/json',
            Cookie: `csrftoken=${csrftoken}`,
            'X-CSRFToken': csrftoken
        }
    });

    const postResponseData = await postResponse.json();

    if (!postResponse.ok) {
        return { errors: { message: postResponseData.detail } };
    }

    // finally set both as cookies for later use
    const responseCookies = postResponse.headers.get('set-cookie');
    responseCookies && setHeaders({ 'set-cookie': [responseCookies, csrfCookie] });
    const next = url.searchParams.get('next') || '/';

    return { location: next };
};
