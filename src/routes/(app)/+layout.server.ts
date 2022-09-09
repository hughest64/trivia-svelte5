import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

export const load: PageServerLoad = async ({ locals, url }) => {
    if (url.pathname === '/favicon.ico') return;
    console.log('running layout.server');

    // TODO: only run under what conditions?
    const response = await fetch(`${apiHost}${url.pathname}/`, {
        method: 'GET',
        headers: locals.fetchHeaders || {}
    });

    let data = {};
    if (response.ok) {
        const responseData = await response.json();
        data = { ...responseData, ...locals };
    }
    else if (url.pathname !== '/') {
        // TODO: this is only appropriate for unathorized requests we may need
        // to return an error to the page rather than redirecting in other cases
        throw redirect(307, `/?next=${url.pathname}`);
    }

    return data;
};
