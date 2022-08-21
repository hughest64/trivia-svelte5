// import * as cookie from 'cookie';
import { getCookieObject, parseRequestHeaders } from '$lib/utils';
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async({ event, resolve }) => {
    // console.log(event.request.headers);
    const cookies = event.request.headers.get('cookie') || '';
    
    if (cookies.includes('jwt') && cookies.includes('csrftoken')) {
        const cookieObject = getCookieObject(event.request);
        const cookieString = parseRequestHeaders(event.request);

        event.locals.fetchHeaders = {
            'content-type': 'application/json',
            cookie: cookieString,
            'x-csrftoken': cookieObject.csrftoken
        };
    }
    const response = await resolve(event);
    
    return response;
};