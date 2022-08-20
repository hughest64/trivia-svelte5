import { getCookieObject, parseRequestHeaders } from '$lib/utils';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

export const load: PageServerLoad = async ({ params, request, url }) => {
    
    // TODO: I don't think this is supposed to run at all here, maybe related to:
    // https://github.com/sveltejs/kit/issues/5960
    if (url.pathname === '/favicon.ico') return;
    console.log('running layout.server');

    const joincode = params.joincode;
    // TODO: probably better to just pull url.pathname and mimic that an api endpoint
    // advantage is that know if it's host or player data that is requested
    const apiPathname = joincode ? `event/${joincode}` : 'user';

    const cookieObject = getCookieObject(request);
    if (!cookieObject.jwt) {
        throw redirect(303, `/user/login?next=${url.pathname}`);
    }

    const cookieString = parseRequestHeaders(request);
    const response = await fetch(`${apiHost}/${apiPathname}/`, {
        method: 'GET',
        headers: {
            cookie: cookieString,
            'x-csrftoken': cookieObject.csrftoken
        }
    });

    let data = {};
    if (response.ok) {
        data = await response.json();
    } else {
        // TODO: checkStatusCode for the real status code
        throw redirect(307, `/user/login?next=${url.pathname}`);
    }

    return data;
};