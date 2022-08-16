import { error } from '@sveltejs/kit';
import * as cookie from 'cookie';
import { browser } from '$app/env';
import { getFetchConfig } from '$lib/utils';
import type { PageLoad } from './$types';

// TODO for migration: this will need to be moved to +page.ts, however...
// we are currently running this function on the server and setting a cookie header,
// does that mean we could run this in server.js (i.e, GET for page) and use the 
// new setHeaders function

// -or- can this move to +page.server.ts?

const apiHost = import.meta.env.VITE_API_HOST;

export const load: PageLoad = async ({ fetch, session }) => {
    if (browser) return;

    const fetchConfig = getFetchConfig('GET');
    const response = await fetch(`${apiHost}/user/login/`, fetchConfig);

    if (response.ok) {
        const cookies = response.headers.get('set-cookie');
        const csrftoken = (cookies && cookie.parse(cookies)?.csrftoken) || '';
        session.csrftoken = csrftoken;

        return;
    }

    throw error(response.status);
};
