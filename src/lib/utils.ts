import * as cookie from 'cookie';
// import type { LoadOutput } from '@sveltejs/kit'; // TODO: check this path
import type { RouteParams } from '.svelte-kit/types/src/routes/$types'; // TODO: check this path
import { PUBLIC_WEBSOCKET_HOST as cookieMaxAge } from '$env/static/public';

/**
 * parse a requests headers and return a concatenated string of requested headers
 * @param {Request} request
 * @param {string[]} cookieKeys an array of cookies to parse, defaaults to ['jwt', 'csrftoken']
 */
export const parseRequestHeaders = (request: Request, cookieKeys: string[] = ['jwt', 'csrftoken']): HeadersInit => {
    const cookies = request.headers.get('cookie') || '';
    const cookieArry: string[] = [];
    let csrftoken = '';
    if (cookies) {
        const cookieObject = cookie.parse(cookies) || {};
        for (const [key, value] of Object.entries(cookieObject)) {
            cookieKeys.indexOf(key) > -1 && cookieArry.push(`${key}=${value}`);
            if (key === 'csrftoken') {
                csrftoken = value;
            };
        }
    }
    return { cookie: cookieArry.join(';'), 'X-CSRFToken': csrftoken };
};

/**
 * retrive a user's active round and question when the event page loads
 * @param params
 * @param request
 * @returns
 */
export const getEventCookie = (params: RouteParams, request: Request): string => {
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
export const setEventCookie = async (params: RouteParams, request: Request) => {
    const data = await request.json();
    const eventKey = `event-${params.joincode}`;

    return {
        headers: {
            accept: 'application/json',
            'set-cookie': cookie.serialize(eventKey, JSON.stringify(data), {
                path: '/',
                httpOnly: true,
                maxAge: Number(cookieMaxAge) || 60 * 60
            })
        }
    };
};

// TODO: deprecate in favor of parseReqeustHeaders?
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
    headers?: HeadersInit
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
// export const checkStatusCode = (response: Response, next?: string): LoadOutput => {
//     let output: LoadOutput;

//     switch (response.status) {
//         case 500:
//             output = { status: 500 };
//             break;
//         case 404:
//             output = { status: 404 };
//             break;
//         case 401:
//             output = { status: 302, redirect: '/' };
//             break;
//         case 403:
//             output = { status: 302, redirect: '/welcome' };
//             break;
//         case 200:
//         default:
//             output = { status: 200 };
//             break;
//     }
//     if (next && output?.redirect && response.status !== 401) {
//         output.redirect += `?next=${next}`;
//     }

//     return output;
// };
