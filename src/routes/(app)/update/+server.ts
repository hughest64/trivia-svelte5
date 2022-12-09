import type { RequestHandler } from './$types';
import { PUBLIC_COOKIE_MAX_AGE, PUBLIC_SECURE_COOKIE } from '$env/static/public';

export const POST: RequestHandler = async ({ cookies, request }) => {
    const data = await request.json();

    if (data) {
        cookies.set(`event-${data.joincode}`, JSON.stringify({ ...data.activeEventData }), {
            path: '/',
            httpOnly: true,
            secure: Boolean(PUBLIC_SECURE_COOKIE),
            maxAge: Number(PUBLIC_COOKIE_MAX_AGE) || 60 * 60
        });
    }

    return new Response();
};
