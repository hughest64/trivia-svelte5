import { getCookieObject } from '$lib/utils';
import type { Handle, /* HandleFetch 8 */ } from '@sveltejs/kit';

export const handle: Handle = async({ event, resolve }) => {
    console.log('Hello from handle!');
    const cookies = event.request.headers.get('cookie') || '';
    const cookieObject = getCookieObject(event.request);
    
    if (cookies.includes('jwt') && cookies.includes('csrftoken')) {   
        event.locals.fetchHeaders = {
            'content-type': 'application/json',
            cookie: cookies, // cookieString,
            'x-csrftoken': cookieObject.csrftoken
        };
    }

    const joincode = event.params.joincode;
    const eventKey = `event-${joincode}`;
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