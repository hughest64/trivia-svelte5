import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

// one option to prevent this from running unnecessarily, would be to not refererence url.pathname
// directly, a bit janky but somethin like this might work
// however, with this method, we may need to look at invalidate() when redirecting from post
export const load: LayoutServerLoad = async ({ locals, url, fetch }) => {
    console.log('running layout.server');
    let apiEndpoint = '';

    if (!locals.loaded) {
        // TODO: this is not how we should have this in the end!
        apiEndpoint =  url.pathname === '/host/choice' ? '/user' : url.pathname;

        let data = {};

        const response = await fetch(`${apiHost}${apiEndpoint}/`);
    
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
    }
};
