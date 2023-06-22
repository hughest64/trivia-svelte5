import type { RequestHandler } from './$types';
import { env } from '$env/dynamic/private';

// TODO: this endpoint is no longer used and should be deprecated

export const POST: RequestHandler = async ({ cookies, request, url }) => {
    const data = await request.json();

    if (data) {
        cookies.set(`event-${data.joincode}`, JSON.stringify({ ...data.activeEventData }), {
            path: '/',
            httpOnly: true,
            secure: url.protocol === 'https:',
            maxAge: Number(env.PUBLIC_COOKIE_MAX_AGE) || 60 * 60 // default of 1 hour
        });
    }

    return new Response();
};
