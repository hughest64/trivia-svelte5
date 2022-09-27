import type { RequestHandler } from './$types';
import { PUBLIC_COOKIE_MAX_AGE } from '$env/static/public';

export const POST: RequestHandler = async ({ cookies, request }) => {
    const data = await request.json();
    console.log({ ...data.activeData });

    if (data) {
        cookies.set(`event-${data.joincode}`, JSON.stringify({ ...data.activeData }), {
            path: '/',
            httpOnly: true,
            maxAge: Number(PUBLIC_COOKIE_MAX_AGE) || 60 * 60
        });
    }

    return new Response();
};
