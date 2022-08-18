import { getCookieObject, parseRequestHeaders } from '$lib/utils';
import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

export const load: PageServerLoad = async ({ params, request, url }) => {
    // TODO: check params for joincode, if it exists, change fetch endpoint so that we get game data back

    const cookieObject = getCookieObject(request);
    if (!cookieObject.jwt) {
        throw redirect(303, `/user/login?next=${url.pathname}`);
    }

    const cookieString = parseRequestHeaders(request);
    const response = await fetch(`${apiHost}/user/`, {
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
