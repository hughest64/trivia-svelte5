import { browser } from '$app/env';
import { PUBLIC_WEBSOCKET_HOST as apiHost } from '$env/static/public';
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ parent, /** setHeaders, */ url }) => {
    if (browser) {
        const data = await parent();
        // TODO: no worky
        // const cookies = data.fetchHeaders?.cookie || '';
        // cookies && setHeaders({ 'cookie': cookies });
    
        const socket = new WebSocket(`${apiHost}/ws${url.pathname}?jwt=${data.jwt}`);
        return { socket };
    }
};