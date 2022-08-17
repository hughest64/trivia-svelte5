import * as cookie from 'cookie';
import { error } from '@sveltejs/kit';
import { getFetchConfig } from '$lib/utils';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ setHeaders }) => {
    const fetchConfig = getFetchConfig('GET');
    const response = await fetch(`${apiHost}/user/login/`, fetchConfig);

    if (!response.ok) {
        throw error(response.status);
    }
    const cookies = response.headers.get('set-cookie');
    const csrftoken = (cookies && cookie.parse(cookies)?.csrftoken) || '';

    setHeaders({ 'set-cookie': cookies });

    return { data: { csrftoken } };
};

export const POST: Action = async ({ request, setHeaders }) => {
    const data = await request.formData();
    const username = data.get('username') || 'guest'; // TODO: remove the fallback!
    const password = data.get('password') || 'guest';
    
    const cookies = request.headers.get('cookie');
    const csrftoken = (cookies && cookie.parse(cookies)?.csrftoken) || '';
    const response = await fetch(`${apiHost}/user/login/`, {
        method: 'POST',
        // credentials: 'include',
        headers: {
            accept: 'application/json',
            'content-type': 'application/json',
            Cookie: `csrftoken=${csrftoken}`,
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            username,
            password
        })
    });
    
    if (!response.ok) {
        throw error(403);
    }

    // TODO: cannot set another set-cookie header (contrary to the docs):
    // https://kit.svelte.dev/docs/load#input-methods-setheaders
    // source of the issue is here:
    // setHeaders (file:///home/todd/dev/tm-svelte/node_modules/@sveltejs/kit/src/runtime/server/index.js:146:12)
    // const responseCookies = response.headers.get('set-cookie');
    // responseCookies && setHeaders({ 'set-cookie': responseCookies });
};
