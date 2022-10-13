import { redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { LayoutServerLoad } from './$types';


export const load: LayoutServerLoad = async ({ locals, url, fetch }) => {
    console.log('running layout.server');

    // TODO: this is not how we should have this in the end!
    const apiEndpoint = url.pathname === '/host/choice' ? '/user' : url.pathname;

    let data = {};

    // TODO: by virtue of accessing url.pathname this will run on every navigation
    // how to determine when to not run?
    const response = await fetch(`${apiHost}${apiEndpoint}/`);

    if (response.ok) {
        const responseData = await response.json();
        data = { ...responseData, ...locals };

    } else if (url.pathname !== '/') {
        // TODO: this is only appropriate for unathorized requests we may need
        // to return an error to the page rather than redirecting in other cases
        throw redirect(307, `/?next=${url.pathname}`);
    }

    return data;
};
