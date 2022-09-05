import * as cookie from 'cookie';

export const getCookieObject = (request: Request): Record<string, string> => {
    const cookies = request.headers.get('cookie') || '';
    const cookieObject = cookie.parse(cookies) || {};

    return cookieObject;
};

/**
 * parse a requests headers and return a concatenated string of requested headers
 * @param {Request} request
 * @param {string[]} cookieKeys an array of cookies to parse, defaaults to ['jwt', 'csrftoken']
 */
export const parseRequestHeaders = (request: Request, cookieKeys: string[] = ['jwt', 'csrftoken']): string => {
    const cookieObject = getCookieObject(request);
    const cookieArry: string[] = [];

    for (const [key, value] of Object.entries(cookieObject)) {
        cookieKeys.indexOf(key) > -1 && cookieArry.push(`${key}=${value}`);
    }

    return cookieArry.join(';');
};

/**
 * take one or many cookie keys and invalidate them by creating new cookies with an exipiration
 * at the beginning of the time epoch
 * @param keys a single cookie key or multiple keys in an array
 * @returns an array of cookies to invalidate (delete)
 */
export const invalidateCookies = (keys: string | string[]): string[] => {
    const blankCookies: string[] = [];

    if (!Array.isArray(keys)) {
        keys = [keys];
    }
    keys.forEach((key) => {
        blankCookies.push(cookie.serialize(key, '', { path: '/', expires: new Date(0) }));
    });

    return blankCookies;
};

/**
 * retrive a user's active round and question when the event page loads
 * @param params
 * @param request
 * @returns
 */
export const getEventCookie = (joincode: string, request: Request): Record<string, string|number> => {
    const cookies = cookie.parse(request.headers.get('cookie') || '');
    const eventKey = `event-${joincode}`;
    const eventCookie = JSON.parse(cookies[eventKey] || '{}');

    return eventCookie;
};

// TODO: investigate where this is used, maybe we can deprecate this
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

export interface SocketConfig {
    socketUrl: string
    token?: string
    retryInterval: number
    // interval?: ReturnType<typeof setTimeout>
    maxRetries: number
    retries: number
}

// TODO: consider a class here, pehaps one that extends WebSocket?
let interval: ReturnType<typeof setTimeout>;
export const createSocket = (socketConfig: SocketConfig) => {
    const { socketUrl, retryInterval, maxRetries, retries } = socketConfig;

    const webSocket = new WebSocket(socketUrl);

    webSocket.onopen = () => {
        clearInterval(interval);
        // TODO: socket.send token?
    };
  
    webSocket.onclose = (event) => {
        if (!event.wasClean && retries <= maxRetries) {
            setTimeout(() => createSocket({ ...socketConfig, retries: retries + 1 }), retryInterval);

        } else {
            // TODO: We could set a message letting the user know the connection died
            clearTimeout(interval);
        }
    };
    // TODO: add onmessage here?
    return webSocket;
};