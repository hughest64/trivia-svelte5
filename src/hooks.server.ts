import { getCookieObject } from '$lib/utils';
import type { Handle, HandleFetch } from '@sveltejs/kit';

// TODO: perhaps a jwt parsing lib is useful to detect user info and set it
// in locals, just basic info like:
// - username
// - is_staff
// - expiration of token
export const handle: Handle = async({ event, resolve }) => {
    // TODO: This may work so we can eliminate the getCookieObject function
    // console.log(event.cookies.get('event-4569'));
    // console.log('csrf:', event.cookies.get('csrftoken'));
    // console.log('jwt:', event.cookies.get('jwt'));
    // console.log(event.request.headers)

    const cookies = event.request.headers.get('cookie') || '';
    const cookieObject = getCookieObject(event.request);
    
    if (cookies.includes('jwt') && cookies.includes('csrftoken')) {   
        event.locals.fetchHeaders = {
            'content-type': 'application/json',
            cookie: cookies,
            'x-csrftoken': cookieObject.csrftoken
        };
        event.locals.loaded = true;
    }

    const joincode = event.params.joincode;
    const eventKey = `event-${joincode}`;
    if (joincode && cookieObject[eventKey]) {
        const { activeRoundNumber, activeQuestionNumber } = JSON.parse(cookieObject[eventKey]);
        event.locals.activeRoundNumber = activeRoundNumber || '';
        event.locals.activeQuestionNumber = activeQuestionNumber || '';
    }
    const response = await resolve(event);
    
    return response;
};

export const handleFetch: HandleFetch = async ({ event, request }) => {
    const requestMod = new Request(request.url,
        {
            method: request.method,
            headers: event.locals.fetchHeaders, // TODO: we should probably merge existing headers
            body: request.body
        }    
    );

    return fetch(requestMod);
};