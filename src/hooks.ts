// import * as cookie from 'cookie';
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async({ event, resolve }) => {
    // event.request.headers.delete('cookie');
    // console.log(event.request.headers);
    const response = await resolve(event);
    // // remove cookies
    // const jwt = cookie.serialize('jwt', '', { expires: new Date() });
    // const csrf = cookie.serialize('csrftoken', '', { expires: new Date(Date.now() - 3600) });
    // response.headers.set('set-cookie', jwt);
    // response.headers.set('set-cookie', csrf);
    
    return response;
};