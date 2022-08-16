import * as cookie from 'cookie';
import { browser } from '$app/env';
import { userdata, type UserData } from '$stores/user';
import { checkStatusCode, getFetchConfig, setCsrfHeaders } from '$lib/utils';
import type { PageLoad } from '@sveltejs/kit';

// TODO for migration: this will need to be moved to +page.ts, however...
// we are currently running this function on the server and setting a cookie header,
// does that mean we could run this in server.js (i.e, GET for page) and use the 
// new setHeaders function

const apiHost = import.meta.env.VITE_API_HOST;

export const load: PageLoad = async ({ fetch, session }) => {
    if (browser) {
        throw new Error("@migration task: Migrate this return statement (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292693)");
        return { status: 200 };
    }

    const fetchConfig = getFetchConfig('GET');
    const response = await fetch(`${apiHost}/user/login/`, fetchConfig);

    if (response.ok) {
        const cookies = response.headers.get('set-cookie');
        const csrftoken = (cookies && cookie.parse(cookies)?.csrftoken) || '';
        session.csrftoken = csrftoken;
    }

    throw new Error("@migration task: Migrate this return statement (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292693)");
    return checkStatusCode(response);
};
