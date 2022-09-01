import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

export const load: PageServerLoad = async ({ locals, params, url }) => {
    
    // TODO: I don't think this is supposed to run at all here, maybe related to:
    // https://github.com/sveltejs/kit/issues/5960 it was not!, this happens on a failed log in attempt
    if (url.pathname === '/favicon.ico') return;
    console.log('running layout.server');

    const joincode = params.joincode;

    // TODO: is it better to just pull url.pathname and mimic that an api endpoint
    // advantage is that know if it's host or player data that is requested
    const apiPathname = joincode ? `event/${joincode}` : 'user';

    const response = await fetch(`${apiHost}/${apiPathname}/`, {
        method: 'GET',
        headers: locals.fetchHeaders || {}
    });

    let data = {};
    if (response.ok) {
        const responseData = await response.json();
        data = { ...responseData, ...locals };

    } else if (url.pathname !== '/') {
        // TODO: checkStatusCode for the real status code
        throw redirect(307, `/?next=${url.pathname}`);
    }

    return data;
};
