import type { Handle } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
import { getFetchConfig } from '$lib/utils';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

export const handle: Handle = async({ event, resolve }) => {
    if (!event.locals.csrfCookie) {
        const fetchConfig = getFetchConfig('GET');
        const response = await fetch(`${apiHost}/user/login/`, fetchConfig);
    
        if (!response.ok) {
            throw error(response.status);
        }
        const csrfcookie = response.headers.get('set-cookie') || '';
    
        if (csrfcookie) {
            event.locals.csrfCookie = csrfcookie;
        };
    }

    return resolve(event);
};