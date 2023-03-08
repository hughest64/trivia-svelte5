import type { RequestHandler } from './$types';
import { env } from '$env/dynamic/private';

export const POST: RequestHandler = async ({ cookies, request }) => {
    const data = await request.json();

    if (data) {
        cookies.set(`event-${data.joincode}`, JSON.stringify({ ...data.activeEventData }), {
            path: '/',
            httpOnly: true,
            secure: Boolean(env.PUBLIC_SECURE_COOKIE),
            maxAge: Number(env.PUBLIC_COOKIE_MAX_AGE) || 60 * 60
        });
    }

    return new Response();
};
