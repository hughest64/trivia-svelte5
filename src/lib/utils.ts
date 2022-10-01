import { getContext, setContext } from 'svelte';
import { writable, type Writable } from 'svelte/store';
import type { Cookies } from '@sveltejs/kit';
import * as cookie from 'cookie';

import type { StoreKey } from './types';

// TODO: review which, if any, functions are still useful

export const getCookieObject = (request: Request): Record<string, string> => {
    const cookies = request.headers.get('cookie') || '';
    const cookieObject = cookie.parse(cookies) || {};

    return cookieObject;
};

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
 * convenience method which sets standard fetch request config values
 *
 * @param method an http method
 * @param data post body data
 * @param headers http headers
 * @returns config object passed to a fetch request
 */
export const getFetchConfig = (method: string, data?: Record<string, unknown>, headers?: HeadersInit): RequestInit => {
    const requestHeaders: Record<string, unknown> = {
        'content-type': 'application/json',
        accept: 'application/json'
    };
    headers && Object.assign(requestHeaders, headers);

    return {
        method,
        credentials: 'include',
        headers: <HeadersInit>requestHeaders,
        body: data && JSON.stringify(data)
    };
};

export function createStore<T>(key: StoreKey, data: T): Writable<T> {
    return setContext(key, writable(data));
}

export function getStore<T>(key: StoreKey): Writable<T> {
    return getContext(key);
}
