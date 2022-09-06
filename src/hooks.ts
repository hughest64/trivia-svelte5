// import * as cookie from 'cookie';
import { getCookieObject, /** parseRequestHeaders */ } from '$lib/utils';
import type { Handle, /* HandleFetch **/ } from '@sveltejs/kit';

export const handle: Handle = async({ event, resolve }) => {
    // console.log(event.request.headers);
    // const cookies = event.request.headers.get('cookie') || '';
    // const cookieString = parseRequestHeaders(event.request);
    const cookieObject = getCookieObject(event.request);
    const joincode = event.params.joincode;
    const eventKey = `event-${joincode}`;
    
    // if (cookies.includes('jwt') && cookies.includes('csrftoken')) {

    //     event.locals.fetchHeaders = {
    //         'content-type': 'application/json',
    //         cookie: cookieString,
    //         'x-csrftoken': cookieObject.csrftoken
    //     };
    //     event.locals.jwt = cookieObject.jwt || '';
    // }
    if (joincode && cookieObject[eventKey]) {
        const { initialRoundNumber, initialQuestionNumber } = JSON.parse(cookieObject[eventKey]);
        event.locals.initialRoundNumber = initialRoundNumber || '';
        event.locals.initialQuestionNumber = initialQuestionNumber || '';
    }
    const response = await resolve(event);
    
    return response;
};

// export const handleFetch: HandleFetch = ({ event, request, fetch }) => {
//     console.log(request.headers);
//     return fetch(request);
// };