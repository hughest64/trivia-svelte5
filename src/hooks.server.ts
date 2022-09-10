// import * as cookie from 'cookie';
import { getCookieObject, parseRequestHeaders } from '$lib/utils';
import type { Handle, /** HandleFetch 8 */ } from '@sveltejs/kit';

// TODO: just use the cookie api to get existing cookies
export const handle: Handle = async({ event, resolve }) => {
    console.log('Hello from handle!');
    const cookies = event.request.headers.get('cookie') || '';
    const cookieString = parseRequestHeaders(event.request);
    const cookieObject = getCookieObject(event.request);
    const joincode = event.params.joincode;
    const eventKey = `event-${joincode}`;
    
    if (cookies.includes('jwt') && cookies.includes('csrftoken')) {

        event.locals.fetchHeaders = {
            'content-type': 'application/json',
            cookie: cookieString,
            'x-csrftoken': cookieObject.csrftoken
        };
        // event.locals.jwt = cookieObject.jwt || '';
    }
    if (joincode && cookieObject[eventKey]) {
        const { initialRoundNumber, initialQuestionNumber } = JSON.parse(cookieObject[eventKey]);
        event.locals.initialRoundNumber = initialRoundNumber || '';
        event.locals.initialQuestionNumber = initialQuestionNumber || '';
    }
    const response = await resolve(event);
    
    return response;
};

// export const handleFetch: HandleFetch = async ({request, fetch }) => {
//     console.log('Running Handle Fetch'); 
//     request.headers.set('test', 'test=does this work?');
//     return fetch(request);
// };