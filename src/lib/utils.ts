import { getContext, setContext } from 'svelte';
import { writable, type Writable } from 'svelte/store';
import type { Cookies } from '@sveltejs/kit';
import { PUBLIC_API_PORT as apiPort } from '$env/static/public';

import type { StoreKey } from './types';

/**
 * take one or many cookie keys and invalidate them by creating new cookies with an exipiration
 * at the beginning of the time epoch
 * @param keys a single cookie key or multiple keys in an array
 * @returns an array of cookies to invalidate (delete)
 */
export const invalidateCookies = (cookies: Cookies, keys: string | string[]): void => {
    if (!Array.isArray(keys)) {
        keys = [keys];
    }
    keys.forEach((key) => {
        cookies.set(key, '', { path: '/', expires: new Date(0) });
    });
};
/**
 * 

 */
export function createStore<T>(key: StoreKey, data: T): Writable<T> {
    return setContext(key, writable(data));
}

export function getStore<T>(key: StoreKey): Writable<T> {
    return getContext(key);
}

/**
 * helper which returns the api or websocket host url from the current page url
 * TODO: this may not actually bes used, I think env variable is the way to go
 */
export function getApiHost(url: URL, pathname='', socket=false): string {
    const isSecure = url.protocol.startsWith('https');
    let protocol = url.protocol;
    
    if (socket) {
        protocol = isSecure ? 'wss:' : 'ws:';
    }
    const hostname = url.hostname;
    const port = url.port ? `:${apiPort}` : '';

    return `${protocol}//${hostname}${port}${pathname || url.pathname}`;
}
