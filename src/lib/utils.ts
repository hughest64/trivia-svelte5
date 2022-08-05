import * as cookie from 'cookie';
import type { LoadOutput, RequestHandlerOutput } from '@sveltejs/kit';

const cookieMaxAge = import.meta.env.VITE_COOKIE_MAX_AGE || 60 * 60; // 1 hour

/**
 * retrive a user's active round and question when the event page loads
 * @param params
 * @param request
 * @returns
 */
export const getEventCookie = (params: Record<string, string>, request: Request): string => {
    const cookies = cookie.parse(request.headers.get('cookie') || '');
    const eventKey = `event-${params.joincode}`;
    const eventCookie = cookies[eventKey] || '{}';

    return eventCookie;
};

/**
 * set a users active round and question in a cookie for reference when the event page loads
 * @param params
 * @param request
 * @returns
 */
export const setEventCookie = async (
    params: Record<string, string>,
    request: Request
): Promise<RequestHandlerOutput> => {
    const data = await request.json();
    const eventKey = `event-${params.joincode}`;

    return {
        headers: {
            accept: 'application/json',
            'set-cookie': cookie.serialize(eventKey, JSON.stringify(data), {
                path: '/',
                httpOnly: true,
                maxAge: cookieMaxAge
            })
        }
    };
};

/**
 * convenience method which creates the necessary
 * headers to include a csrf token in a fetch request
 *
 * @param {string }csrfToken
 * @returns cookie headers for the csrf token
 */
export const setCsrfHeaders = (csrfToken: string): Record<string, string> => {
    return {
        Cookie: `csrftoken=${csrfToken}`,
        // TODO: this probably isn't neccessary!
        'X-CSRFToken': csrfToken
    };
};

/**
 * convenience method which sets standard fetch request config values
 *
 * @param method an http method
 * @param data post body data
 * @param headers http headers
 * @returns config object passed to a fetch request
 */
export const getFetchConfig = (
    method: string,
    data?: Record<string, unknown>,
    headers?: Record<string, unknown>
): RequestInit => {
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

/**
 * Convenience function that handles standard actions as the ouput
 * to a load function based on the response of a fetch call to the api.
 *
 * @param {Response} response the response object of an api fetch call
 * @param {string} next querystring appended to a redirect url
 * @returns {LoadOutput}
 */
export const checkStatusCode = (response: Response, next?: string): LoadOutput => {
    let output: LoadOutput;

    switch (response.status) {
        case 500:
            output = { status: 500 };
            break;
        case 404:
            output = { status: 404 };
            break;
        case 401:
            output = { status: 302, redirect: '/' };
            break;
        case 403:
            output = { status: 302, redirect: '/welcome' };
            break;
        case 200:
        default:
            output = { status: 200 };
            break;
    }
    if (next && output?.redirect && response.status !== 401) {
        output.redirect += `?next=${next}`;
    }

    return output;
};
