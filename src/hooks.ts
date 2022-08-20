// import * as cookie from 'cookie';
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async({ event, resolve }) => {
    // console.log(event.request.headers);
    const response = await resolve(event);
    
    return response;
};