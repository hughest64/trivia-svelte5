import * as cookie from 'cookie';
import { error } from '@sveltejs/kit';
import { getFetchConfig } from '$lib/utils';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import { userdata } from '$stores/user';
import type { UserData } from '$stores/user';
import type {
    Action,
    PageServerLoad
} from './$types';

/**
* TODO: cannot set multiple set-cookie header (contrary to the docs):
* https://kit.svelte.dev/docs/load#input-methods-setheaders
* source of the issue is here:
* setHeaders (file:///home/todd/dev/tm-svelte/node_modules/@sveltejs/kit/src/runtime/server/index.js:146:12)
*/

export const load: PageServerLoad = async ({ request }) => {
    const cookies = request.headers.get('set-cookie') || '';
    const jwt = cookie.parse(cookies)?.jwt;
    if (jwt) {
        // redirect the user, they don't need to log in
    }
};

export const POST: Action = async ({ request, setHeaders, url }) => {
    // TODO: return error if either field is blank (validate)
    const formData = await request.formData();
    const username = formData.get('username') || 'guest'; // TODO: remove the fallback!
    const password = formData.get('password') || 'guest';

    // first, get a csrftoken
    const fetchConfig = getFetchConfig('GET');
    const getResponse = await fetch(`${apiHost}/user/login/`, fetchConfig);

    // TODO: handle error
    if (!getResponse.ok) {
        throw error(getResponse.status);
    }
    const csrfCookie = getResponse.headers.get('set-cookie') || '';
    const csrftoken = (csrfCookie && cookie.parse(csrfCookie)?.csrftoken) || '';

    // TODO: use fetchConfig
    // then use the csrftoken to log in
    const postResponse = await fetch(`${apiHost}/user/login/`, {
        method: 'POST',
        headers: {
            accept: 'application/json',
            'content-type': 'application/json',
            Cookie: `csrftoken=${csrftoken}`,
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ username, password })
    });
    
    if (!postResponse.ok) {
        // TODO: handle error messaging
        throw error(postResponse.status);
    }

    const responseData: UserData = await postResponse.json();
    userdata.set(responseData);

    
    // finally set both as cookies for later use
    const responseCookies = postResponse.headers.get('set-cookie');
    responseCookies && setHeaders({ 'set-cookie': [responseCookies, csrfCookie] });
    
    // console.log(url);
    const next = url.searchParams.get('next') || '/';
    // return { location: 'game/join' };

    return { location: next };
    
};
