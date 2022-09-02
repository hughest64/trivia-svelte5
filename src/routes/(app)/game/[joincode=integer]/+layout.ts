import { browser } from '$app/environment';
import { PUBLIC_API_HOST, PUBLIC_WEBSOCKET_HOST as apiHost } from '$env/static/public';
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ fetch, parent, /** setHeaders, */ url }) => {
    const data = await parent();
    if (browser) {
        const response = await fetch(`${PUBLIC_API_HOST}/user/validate/`,
            {
                method: 'POST',
                credentials: 'include',
                body: JSON.stringify({ jwt: data.jwt }),
                headers: data.fetchHeaders
            }
        );
        console.log(response.headers.get('set-cookie'));
        // TODO: no worky
        // const cookies = data.fetchHeaders?.cookie || '';
        // cookies && setHeaders({ 'cookie': cookies });
    
        // const socket = new WebSocket(`${apiHost}/ws${url.pathname}?jwt=${data.jwt}`);
        // return { socket };
    }
};